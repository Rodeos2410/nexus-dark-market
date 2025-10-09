from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import requests
import os
import json
import random
import string
from config import config
from sqlalchemy import text

# === 1. Создаём глобальные расширения ===
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'

# === 2. Модели (используют db) ===
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    telegram_username = db.Column(db.String(100), nullable=True)  # @username без @
    telegram_chat_id = db.Column(db.String(50), nullable=True)  # chat_id для отправки сообщений
    is_banned = db.Column(db.Boolean, default=False)  # статус блокировки
    is_admin = db.Column(db.Boolean, default=False)  # статус администратора
    auth_code = db.Column(db.String(6), nullable=True)  # код для двухфакторной аутентификации
    auth_code_expires = db.Column(db.DateTime, nullable=True)  # время истечения кода
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    products = db.relationship('Product', backref='seller', lazy=True)
    cart_items = db.relationship('CartItem', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stock = db.Column(db.Integer, default=0)  # количество на складе
    
    def __repr__(self):
        return f'<Product {self.name}>'

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    product = db.relationship('Product', backref='cart_items')
    
    def __repr__(self):
        return f'<CartItem {self.product.name} x{self.quantity}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# === 3. Функция создания приложения ===
def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    db.init_app(app)
    login_manager.init_app(app)
    return app

# === 4. Создаём приложение ===
app = create_app()

# === Telegram уведомления ===
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '8458514538:AAFIAT7BrKelIHie9-JscBnOlAFd_V2qyMY')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '1172834372')  # ID админа для уведомлений

def send_telegram_message(text: str, chat_id: str = None, keyboard: dict = None) -> None:
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': chat_id or TELEGRAM_CHAT_ID,
            'text': text,
            'parse_mode': 'HTML'
        }
        
        # Добавляем клавиатуру, если она есть
        if keyboard:
            payload['reply_markup'] = json.dumps(keyboard)
        
        # Не блокируем основной поток: таймаути короткие
        response = requests.post(url, data=payload, timeout=5)
        if not response.json().get('ok'):
            print(f"Telegram error: {response.json()}")
    except Exception as e:
        # Игнорируем ошибки уведомлений, чтобы не ломать покупку
        print(f"Telegram send error: {e}")
        pass

def edit_telegram_message(text: str, chat_id: str, message_id: int, keyboard: dict = None) -> None:
    """Редактирует сообщение в Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/editMessageText"
        payload = {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        
        # Добавляем клавиатуру, если она есть
        if keyboard:
            payload['reply_markup'] = json.dumps(keyboard)
        
        response = requests.post(url, data=payload, timeout=5)
        if not response.json().get('ok'):
            print(f"Telegram edit error: {response.json()}")
    except Exception as e:
        print(f"Telegram edit error: {e}")

def answer_callback_query(callback_query_id: str, text: str = None) -> None:
    """Отвечает на callback query"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/answerCallbackQuery"
        payload = {
            'callback_query_id': callback_query_id
        }
        
        if text:
            payload['text'] = text
        
        response = requests.post(url, data=payload, timeout=5)
        if not response.json().get('ok'):
            print(f"Telegram callback answer error: {response.json()}")
    except Exception as e:
        print(f"Telegram callback answer error: {e}")

def send_order_notification(items_details, total_amount: float, buyer_name: str) -> None:
    lines = [f"🛒 Новая заявка из корзины", f"Покупатель: <b>{buyer_name}</b>"]
    lines.append("")
    lines.append("Товары:")
    for d in items_details:
        lines.append(f"• {d['name']} — {d['qty']} шт × {d['price']:.2f}₽ = {d['line_total']:.2f}₽")
    lines.append("")
    lines.append(f"Итого: <b>{total_amount:.2f}₽</b>")
    text = "\n".join(lines)
    send_telegram_message(text)

def send_admin_notification(message: str) -> None:
    """Отправляет уведомление админу об управлении товарами"""
    admin_chat_id = "1172834372"  # ID админа
    send_telegram_message(message, admin_chat_id)

def send_seller_notification(product_name: str, quantity: int, price: float, buyer_name: str, seller_telegram: str, seller_chat_id: str = None) -> None:
    """Отправляет уведомление продавцу о покупке его товара"""
    if not seller_chat_id:
        print(f"Не удалось отправить уведомление продавцу {seller_telegram}: нет chat_id. Пользователь должен запустить бота @NexusDarkBot")
        return  # Отправляем только если есть chat_id
    
    lines = [f"💰 <b>Ваш товар куплен!</b>"]
    lines.append("")
    lines.append(f"Товар: <b>{product_name}</b>")
    lines.append(f"Количество: {quantity} шт")
    lines.append(f"Цена за штуку: {price:.2f}₽")
    lines.append(f"Покупатель: <b>{buyer_name}</b>")
    lines.append("")
    lines.append(f"Сумма: <b>{price * quantity:.2f}₽</b>")
    
    text = "\n".join(lines)
    
    # Отправляем только по chat_id
    send_telegram_message(text, seller_chat_id)


def generate_auth_code():
    """Генерирует 6-значный код для двухфакторной аутентификации"""
    return ''.join(random.choices(string.digits, k=6))

def send_auth_code_to_telegram(user, auth_code):
    """Отправляет код аутентификации в Telegram"""
    if not user.telegram_chat_id:
        return False
    
    message = f"🔐 <b>Код для входа в админ панель</b>\n\n"
    message += f"👤 Пользователь: <code>{user.username}</code>\n"
    message += f"🔢 Код: <code>{auth_code}</code>\n\n"
    message += f"⏰ Код действителен 5 минут\n"
    message += f"📋 Нажмите на код для копирования"
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': user.telegram_chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, data=payload, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Ошибка отправки кода в Telegram: {e}")
        return False

def ensure_schema():
    # Создаем все таблицы и добавляем колонки, если их нет
    with app.app_context():
        try:
            # Сначала создаем все таблицы
            print("🔄 Creating database tables...")
            db.create_all()
            
            # Для PostgreSQL используем другой подход
            conn = db.engine.connect()
            
            # Проверяем, какая база данных используется
            db_type = db.engine.url.drivername
            
            if 'postgresql' in db_type:
                print("🗄️ Using PostgreSQL - skipping column checks (tables created by SQLAlchemy)")
                # Для PostgreSQL SQLAlchemy создает все колонки автоматически
                pass
            else:
                # Для SQLite используем PRAGMA
                print("🗄️ Using SQLite - checking columns")
                
                # Проверяем таблицу product
                try:
                    res = conn.execute(text("PRAGMA table_info(product)"))
                    cols = [row[1] for row in res]
                    if 'stock' not in cols:
                        print("🔄 Adding stock column to product table")
                        conn.execute(text("ALTER TABLE product ADD COLUMN stock INTEGER DEFAULT 0"))
                except Exception as e:
                    print(f"⚠️ Product table check failed: {e}")
                
                # Проверяем таблицу user
                try:
                    res = conn.execute(text("PRAGMA table_info(user)"))
                    cols = [row[1] for row in res]
                    print(f"📋 Current user table columns: {cols}")
                    
                    if 'telegram_username' not in cols:
                        print("🔄 Adding telegram_username column to user table")
                        conn.execute(text("ALTER TABLE user ADD COLUMN telegram_username VARCHAR(100)"))
                    if 'telegram_chat_id' not in cols:
                        print("🔄 Adding telegram_chat_id column to user table")
                        conn.execute(text("ALTER TABLE user ADD COLUMN telegram_chat_id VARCHAR(50)"))
                    if 'is_banned' not in cols:
                        print("🔄 Adding is_banned column to user table")
                        conn.execute(text("ALTER TABLE user ADD COLUMN is_banned BOOLEAN DEFAULT 0"))
                            if 'is_admin' not in cols:
                                print("🔄 Adding is_admin column to user table")
                                conn.execute(text("ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT 0"))
                            if 'auth_code' not in cols:
                                print("🔄 Adding auth_code column to user table")
                                conn.execute(text("ALTER TABLE user ADD COLUMN auth_code VARCHAR(6)"))
                            if 'auth_code_expires' not in cols:
                                print("🔄 Adding auth_code_expires column to user table")
                                conn.execute(text("ALTER TABLE user ADD COLUMN auth_code_expires DATETIME"))
                except Exception as e:
                    print(f"⚠️ User table check failed: {e}")
            
            conn.commit()
            conn.close()
            print("✅ Database schema migration completed")
        except Exception as e:
            print(f"❌ Database migration error: {e}")
            # Если миграция не удалась, не блокируем запуск
            pass

with app.app_context():
    # Выполним проверку схемы на этапе импорта (совместимо с Flask>=3)
    ensure_schema()

# === 5. Контекстный процессор ===
@app.context_processor
def inject_cart_data():
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        cart_count = len(cart_items)
        cart_total = sum(item.product.price * item.quantity for item in cart_items)
        return dict(cart_items=cart_items, cart_count=cart_count, cart_total=cart_total)
    return dict(cart_items=[], cart_count=0, cart_total=0)

# === 6. Маршруты ===
@app.route('/')
def index():
    return redirect(url_for('market'))

@app.route('/market')
def market():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('market.html', products=products)

# ... (все остальные маршруты: login, register, logout, profile, add_product, cart, checkout и т.д.)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('market'))
    
    if request.method == 'POST':
        # Проверяем, есть ли код в запросе (вторая стадия аутентификации)
        auth_code = request.form.get('auth_code', '').strip()
        
        if auth_code:
            # Вторая стадия - проверка кода
            username = request.form.get('username', '').strip()
            user = User.query.filter_by(username=username).first()
            
            if user and user.auth_code and user.auth_code_expires:
                # Проверяем, не истек ли код
                if datetime.utcnow() <= user.auth_code_expires:
                    if user.auth_code == auth_code:
                        # Код верный, входим в систему
                        if user.is_banned:
                            flash('Ваш аккаунт заблокирован. Обратитесь к администратору.')
                        else:
                            # Очищаем код после успешного входа
                            user.auth_code = None
                            user.auth_code_expires = None
                            db.session.commit()
                            
                            login_user(user)
                            next_page = request.args.get('next')
                            return redirect(next_page) if next_page else redirect(url_for('market'))
                    else:
                        flash('Неверный код аутентификации')
                else:
                    flash('Код аутентификации истек. Попробуйте войти заново.')
                    # Очищаем истекший код
                    user.auth_code = None
                    user.auth_code_expires = None
                    db.session.commit()
            else:
                flash('Код аутентификации не найден. Попробуйте войти заново.')
        else:
            # Первая стадия - проверка логина и пароля
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
            
            if not username or not password:
                flash('Пожалуйста, заполните все поля')
                return render_template('login.html')
            
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password_hash, password):
                if user.is_banned:
                    flash('Ваш аккаунт заблокирован. Обратитесь к администратору.')
                else:
                    # Генерируем код и отправляем в Telegram
                    auth_code = generate_auth_code()
                    user.auth_code = auth_code
                    user.auth_code_expires = datetime.utcnow() + timedelta(minutes=5)
                    db.session.commit()
                    
                    # Отправляем код в Telegram
                    if send_auth_code_to_telegram(user, auth_code):
                        flash('Код аутентификации отправлен в Telegram. Введите его ниже.')
                        return render_template('login.html', show_code_input=True, username=username)
                    else:
                        flash('Ошибка отправки кода в Telegram. Проверьте настройки уведомлений.')
                        # Очищаем код при ошибке отправки
                        user.auth_code = None
                        user.auth_code_expires = None
                        db.session.commit()
            else:
                flash('Неверное имя пользователя или пароль')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('market'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        if not all([username, email, password, confirm_password]):
            flash('Пожалуйста, заполните все поля')
            return render_template('register.html')
        if len(username) < 3:
            flash('Имя пользователя должно содержать минимум 3 символа')
            return render_template('register.html')
        if len(password) < 6:
            flash('Пароль должен содержать минимум 6 символов')
            return render_template('register.html')
        if password != confirm_password:
            flash('Пароли не совпадают')
            return render_template('register.html')
        if User.query.filter_by(username=username).first():
            flash('Пользователь с таким именем уже существует')
            return render_template('register.html')
        if User.query.filter_by(email=email).first():
            flash('Пользователь с таким email уже существует')
            return render_template('register.html')
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            balance=0
        )
        try:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Регистрация прошла успешно! Добро пожаловать!')
            return redirect(url_for('market'))
        except Exception as e:
            db.session.rollback()
            flash('Произошла ошибка при регистрации. Попробуйте еще раз.')
            return render_template('register.html')
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы')
    return redirect(url_for('market'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        telegram_username = request.form.get('telegram_username', '').strip()
        # Убираем @ если пользователь его ввел
        if telegram_username.startswith('@'):
            telegram_username = telegram_username[1:]
        
        current_user.telegram_username = telegram_username if telegram_username else None
        try:
            db.session.commit()
            if telegram_username:
                flash(f'Telegram username @{telegram_username} сохранен! Теперь перейдите к боту @NexusDarkBot и отправьте /start')
            else:
                flash('Telegram username удален')
        except Exception:
            db.session.rollback()
            flash('Ошибка при обновлении профиля')
    
    return render_template('profile.html')

@app.route('/users')
def users():
    users_list = User.query.order_by(User.created_at.desc()).all()
    return render_template('users.html', users=users_list)

@app.route('/admin')
@login_required
def admin_panel():
    """Админская панель"""
    if not current_user.is_admin:
        flash('Доступ запрещен')
        return redirect(url_for('market'))
    
    users_list = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin.html', users=users_list)

@app.route('/admin/user/<int:user_id>/ban', methods=['POST'])
@login_required
def ban_user(user_id):
    """Заблокировать пользователя"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Доступ запрещен'}), 403
    
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        return jsonify({'success': False, 'message': 'Нельзя заблокировать самого себя'})
    
    user.is_banned = True
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': f'Пользователь {user.username} заблокирован'})
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Ошибка при блокировке'})

@app.route('/admin/user/<int:user_id>/unban', methods=['POST'])
@login_required
def unban_user(user_id):
    """Разблокировать пользователя"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Доступ запрещен'}), 403
    
    user = User.query.get_or_404(user_id)
    user.is_banned = False
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': f'Пользователь {user.username} разблокирован'})
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Ошибка при разблокировке'})

@app.route('/admin/user/<int:user_id>/make_admin', methods=['POST'])
@login_required
def make_admin(user_id):
    """Сделать пользователя администратором"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Доступ запрещен'}), 403
    
    user = User.query.get_or_404(user_id)
    user.is_admin = True
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': f'Пользователь {user.username} назначен администратором'})
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Ошибка при назначении администратором'})

@app.route('/admin/user/<int:user_id>/remove_admin', methods=['POST'])
@login_required
def remove_admin(user_id):
    """Убрать права администратора"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Доступ запрещен'}), 403
    
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        return jsonify({'success': False, 'message': 'Нельзя убрать права администратора у самого себя'})
    
    user.is_admin = False
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': f'Права администратора убраны у {user.username}'})
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Ошибка при снятии прав администратора'})

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        price_str = request.form.get('price', '0')
        stock_str = request.form.get('stock', '0')
        if not name:
            flash('Пожалуйста, укажите название товара')
            return render_template('add_product.html')
        try:
            price = float(price_str)
            if price <= 0:
                flash('Цена должна быть положительным числом')
                return render_template('add_product.html')
        except ValueError:
            flash('Неверный формат цены')
            return render_template('add_product.html')
        try:
            stock = int(stock_str)
            if stock < 0:
                flash('Количество не может быть отрицательным')
                return render_template('add_product.html')
        except ValueError:
            flash('Неверный формат количества')
            return render_template('add_product.html')
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
                if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                    filename = secure_filename(file.filename)
                    timestamp = str(int(datetime.now().timestamp()))
                    name_part, ext_part = filename.rsplit('.', 1)
                    filename = f"{timestamp}_{name_part}.{ext_part}"
                    try:
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        image_filename = filename
                    except Exception as e:
                        flash('Ошибка при загрузке изображения')
                        return render_template('add_product.html')
                else:
                    flash('Неподдерживаемый формат изображения. Используйте PNG, JPG, JPEG, GIF или WebP')
                    return render_template('add_product.html')
        product = Product(
            name=name,
            description=description,
            price=price,
            image=image_filename,
            seller_id=current_user.id,
            stock=stock
        )
        try:
            db.session.add(product)
            db.session.commit()
            
            # Отправляем уведомление админу о добавлении товара
            admin_message = f"📦 <b>Новый товар добавлен</b>\n\nТовар: <b>{product.name}</b>\nПродавец: <b>{current_user.username}</b>\nЦена: {product.price}₽\nОстаток: {product.stock} шт"
            send_admin_notification(admin_message)
            
            flash('Товар успешно добавлен!')
            return redirect(url_for('market'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при добавлении товара')
            # После ошибки тоже показываем список товаров ниже
            user_products = Product.query.filter_by(seller_id=current_user.id).order_by(Product.created_at.desc()).all()
            return render_template('add_product.html', products=user_products)
    # GET — показать форму и список своих товаров
    user_products = Product.query.filter_by(seller_id=current_user.id).order_by(Product.created_at.desc()).all()
    return render_template('add_product.html', products=user_products)

@app.route('/product/<int:product_id>/delete', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.seller_id != current_user.id:
        return jsonify({'success': False, 'message': 'Нет прав на удаление'}), 403
    # удаляем файл изображения, если есть
    if product.image:
        try:
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], product.image)
            if os.path.exists(img_path):
                os.remove(img_path)
        except Exception:
            pass
    try:
        # Отправляем уведомление админу об удалении товара
        admin_message = f"🗑️ <b>Товар удален</b>\n\nТовар: <b>{product.name}</b>\nПродавец: <b>{current_user.username}</b>\nЦена: {product.price}₽"
        send_admin_notification(admin_message)
        
        db.session.delete(product)
        db.session.commit()
        return jsonify({'success': True})
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Ошибка при удалении'}), 500

@app.route('/product/<int:product_id>/update', methods=['POST'])
@login_required
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.seller_id != current_user.id:
        return jsonify({'success': False, 'message': 'Нет прав на редактирование'}), 403
    name = request.form.get('name', product.name).strip()
    description = request.form.get('description', product.description or '').strip()
    price_str = request.form.get('price', str(product.price))
    stock_str = request.form.get('stock', str(product.stock if product.stock is not None else 0))
    try:
        price = float(price_str)
        if price <= 0:
            return jsonify({'success': False, 'message': 'Цена должна быть > 0'})
    except ValueError:
        return jsonify({'success': False, 'message': 'Неверная цена'})
    try:
        stock_val = int(stock_str)
        if stock_val < 0:
            return jsonify({'success': False, 'message': 'Остаток не может быть отрицательным'})
    except ValueError:
        return jsonify({'success': False, 'message': 'Неверное количество'})
    product.name = name or product.name
    product.description = description
    product.price = price
    product.stock = stock_val
    # опционально можно обновить картинку
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename:
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
            if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                filename = secure_filename(file.filename)
                timestamp = str(int(datetime.now().timestamp()))
                name_part, ext_part = filename.rsplit('.', 1)
                filename = f"{timestamp}_{name_part}.{ext_part}"
                try:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    # удалить старое изображение
                    if product.image:
                        old = os.path.join(app.config['UPLOAD_FOLDER'], product.image)
                        if os.path.exists(old):
                            os.remove(old)
                    product.image = filename
                except Exception:
                    return jsonify({'success': False, 'message': 'Ошибка загрузки изображения'})
            else:
                return jsonify({'success': False, 'message': 'Неверный формат изображения'})
    try:
        db.session.commit()
        return jsonify({'success': True})
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Ошибка при сохранении'})

@app.route('/cart/update/<int:product_id>', methods=['POST'])
@login_required
def update_cart(product_id):
    data = request.get_json()
    qty = data.get('quantity', 1)
    try:
        qty = int(qty)
    except:
        return jsonify({'success': False, 'message': 'Неверное количество'})
    item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if not item:
        return jsonify({'success': False, 'message': 'Товар не в корзине'})
    if qty < 1:
        db.session.delete(item)
    else:
        item.quantity = qty
    try:
        db.session.commit()
        return jsonify({'success': True})
    except:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Ошибка при обновлении'})

@app.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    if product.seller_id == current_user.id:
        return jsonify({'success': False, 'message': 'Нельзя добавить свой товар в корзину'})
    if product.stock is not None and product.stock <= 0:
        return jsonify({'success': False, 'message': 'Товара нет в наличии'})
    existing = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing:
        existing.quantity += 1
    else:
        db.session.add(CartItem(user_id=current_user.id, product_id=product_id))
    try:
        # уменьшать склад сразу не будем, только при checkout
        db.session.commit()
        return jsonify({'success': True})
    except:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Ошибка при добавлении в корзину'})

@app.route('/cart/remove/<int:product_id>', methods=['POST'])
@login_required
def remove_from_cart(product_id):
    item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if item:
        try:
            db.session.delete(item)
            db.session.commit()
            return jsonify({'success': True})
        except:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Ошибка при удалении из корзины'})
    return jsonify({'success': False, 'message': 'Товар не найден в корзине'})

@app.route('/cart/list', methods=['GET'])
@login_required
def list_cart():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    result = []
    total = 0.0
    for item in items:
        line_total = float(item.product.price) * int(item.quantity)
        total += line_total
        result.append({
            'productId': item.product.id,
            'name': item.product.name,
            'price': float(item.product.price),
            'quantity': int(item.quantity),
            'lineTotal': line_total
        })
    return jsonify({
        'success': True,
        'items': result,
        'count': len(items),
        'total': total
    })

@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        return jsonify({'success': False, 'message': 'Корзина пуста'})
    # проверим наличие на складе
    for item in cart_items:
        if item.product.stock is not None and item.quantity > item.product.stock:
            return jsonify({'success': False, 'message': f'Недостаточно на складе для {item.product.name}'})
    total = sum(item.product.price * item.quantity for item in cart_items)
    if current_user.balance < total:
        return jsonify({
            'success': False,
            'message': f'Недостаточно средств. Нужно {total:.2f}₽, а у вас {current_user.balance:.2f}₽'
        })
    # подготовим информацию для уведомления до удаления позиций из корзины
    items_details = []
    for item in cart_items:
        line_total = float(item.product.price) * int(item.quantity)
        items_details.append({
            'name': item.product.name,
            'qty': int(item.quantity),
            'price': float(item.product.price),
            'line_total': line_total
        })

    try:
        current_user.balance -= total
        for item in cart_items:
            # списываем склад
            if item.product.stock is not None:
                item.product.stock = max(0, int(item.product.stock) - int(item.quantity))
            db.session.delete(item)
        db.session.commit()
        
        # отправляем уведомления продавцам товаров
        try:
            for item in cart_items:
                seller = item.product.seller
                if seller and seller.telegram_chat_id:
                    send_seller_notification(
                        product_name=item.product.name,
                        quantity=item.quantity,
                        price=float(item.product.price),
                        buyer_name=current_user.username,
                        seller_telegram=seller.telegram_username,
                        seller_chat_id=seller.telegram_chat_id
                    )
        except Exception:
            pass
        return jsonify({
            'success': True,
            'message': f'Покупка на сумму {total:.2f}₽ совершена успешно!'
        })
    except:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Ошибка при обработке покупки'})

@app.route('/deposit', methods=['POST'])
@login_required
def deposit():
    data = request.get_json()
    amount = data.get('amount', 0)
    if amount > 0 and amount <= 10000:
        try:
            current_user.balance += amount
            db.session.commit()
            return jsonify({'success': True, 'message': f'Баланс пополнен на {amount}₽'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Ошибка при пополнении баланса'})
    return jsonify({'success': False, 'message': 'Неверная сумма пополнения'})



@app.route('/telegram/webhook', methods=['POST'])
def telegram_webhook():
    """Webhook для получения обновлений от Telegram бота"""
    try:
        data = request.get_json()
        print(f"🔍 Webhook received: {data}")  # Отладочная информация
        
        if not data:
            print("❌ No data in webhook")
            return jsonify({'ok': True})
        
        # Обрабатываем callback_query (нажатия на кнопки)
        if 'callback_query' in data:
            from telegram_bot import handle_callback_query, answer_callback_query
            callback_query = data['callback_query']
            chat_id = str(callback_query['message']['chat']['id'])
            message_id = callback_query['message']['message_id']
            
            print(f"🔘 Callback: {callback_query['data']} from {chat_id}")
            
            # Обрабатываем только админские callback
            if chat_id == '1172834372':
                response, keyboard = handle_callback_query(callback_query, chat_id)
                
                # Отвечаем на callback query
                answer_callback_query(callback_query['id'])
                
                # Редактируем сообщение
                edit_telegram_message(response, chat_id, message_id, keyboard)
            
            return jsonify({'ok': True})
        
        # Обрабатываем обычные сообщения
        if 'message' not in data:
            print("❌ No message in webhook data")
            return jsonify({'ok': True})
        
        message = data['message']
        chat_id = str(message['chat']['id'])
        username = message['from'].get('username', '')
        text = message.get('text', '')
        
        print(f"📱 Chat ID: {chat_id}, Username: {username}, Text: {text}")
        
        # Обрабатываем админ команды
        if chat_id == '1172834372':
            from telegram_bot import handle_admin_command
            response, keyboard = handle_admin_command(text, chat_id)
            send_telegram_message(response, chat_id, keyboard)
            return jsonify({'ok': True})
        
        # Обрабатываем команды пользователей
        if text.startswith('/start'):
            # Извлекаем параметр из команды /start (если есть)
            start_param = text.split(' ', 1)[1] if ' ' in text else None
            
            if start_param == 'get_id':
                # Отправляем пользователю его Chat ID
                id_message = f"🆔 <b>Ваш Chat ID:</b>\n\n<code>{chat_id}</code>\n\n📋 <b>Как скопировать:</b>\n• Нажмите на ID выше\n• Или выделите и скопируйте вручную\n\n🔧 <b>Что дальше:</b>\n1. Скопируйте этот ID\n2. Вставьте в поле на сайте\n3. Нажмите 'Настроить'"
                send_telegram_message(id_message, chat_id)
                return jsonify({'ok': True})
            
            else:
                # Обычный /start - отправляем инструкции
                welcome_message = f"""🆔 <b>Ваш Chat ID:</b>

<code>{chat_id}</code>

📋 <b>Как скопировать:</b>
• Нажмите на ID выше
• Или выделите и скопируйте вручную

🔧 <b>Что дальше:</b>
1. Скопируйте этот ID
2. Вставьте в поле на сайте Nexus Dark
3. Нажмите 'Настроить'

✅ <b>Готово!</b> Вы будете получать уведомления о продажах ваших товаров.

💡 <b>Команды:</b>
/start - Получить Chat ID"""
                
                send_telegram_message(welcome_message, chat_id)
                return jsonify({'ok': True})
        
        elif text and not text.startswith('/'):
            # На любое другое сообщение отправляем инструкции
            unknown_message = f"""🆔 <b>Ваш Chat ID:</b>

<code>{chat_id}</code>

📋 <b>Как скопировать:</b>
• Нажмите на ID выше
• Или выделите и скопируйте вручную

🔧 <b>Что дальше:</b>
1. Скопируйте этот ID
2. Вставьте в поле на сайте Nexus Dark
3. Нажмите 'Настроить'

✅ <b>Готово!</b> Вы будете получать уведомления о продажах ваших товаров.

💡 <b>Команды:</b>
/start - Получить Chat ID"""
            
            send_telegram_message(unknown_message, chat_id)
            return jsonify({'ok': True})
        
        if username:
            # Старый способ: поиск по username (для обратной совместимости)
            user = User.query.filter_by(telegram_username=username).first()
            if user:
                # Проверяем, не настроены ли уже уведомления
                if user.telegram_chat_id:
                    already_setup_text = f"Привет, {user.username}! 👋\n\n✅ <b>Уведомления уже настроены!</b>\n\n📱 Username: @{username}\n🆔 Chat ID: {user.telegram_chat_id}\n\nВы будете получать уведомления о продажах ваших товаров в Nexus Dark!"
                    send_telegram_message(already_setup_text, chat_id)
                else:
                    # Сохраняем chat_id в базе данных
                    user.telegram_chat_id = chat_id
                    db.session.commit()
                    print(f"User {username} started bot, chat_id: {chat_id}")
                    
                    # Отправляем приветственное сообщение
                    welcome_text = f"Привет, {user.username}! 🎉\n\n✅ <b>Telegram уведомления настроены!</b>\n\nТеперь вы будете получать уведомления о продажах ваших товаров в Nexus Dark!\n\n📱 Ваш username: @{username}\n🆔 Chat ID: {chat_id}\n\n🎯 <b>Что дальше?</b>\n• Добавляйте товары на продажу\n• Получайте уведомления о покупках\n• Используйте кнопку 'Тест Telegram' в профиле"
                    send_telegram_message(welcome_text, chat_id)
            else:
                # Пользователь не найден в базе
                not_found_text = f"❌ <b>Пользователь не найден</b>\n\nВаш Telegram username: <b>@{username}</b>\n\n🔧 <b>Чтобы получать уведомления:</b>\n1. Зайдите на сайт <b>Nexus Dark</b>\n2. Войдите в свой аккаунт\n3. Перейдите в <b>Профиль</b>\n4. Укажите ваш Telegram username: <b>{username}</b>\n5. Сохраните изменения\n6. Отправьте <b>/start</b>"
                send_telegram_message(not_found_text, chat_id)
        else:
            # У пользователя нет username
            no_setup_text = "❌ <b>У вас не указан Telegram username</b>\n\n🔧 <b>Чтобы получать уведомления:</b>\n1. Зайдите в <b>настройки Telegram</b>\n2. Установите <b>username</b>\n3. Зайдите на сайт <b>Nexus Dark</b>\n4. Укажите username в <b>профиле</b>\n5. Отправьте <b>/start</b>"
            send_telegram_message(no_setup_text, chat_id)
        
        if text == '/check':
            if username:
                # Ищем пользователя по telegram_username
                user = User.query.filter_by(telegram_username=username).first()
                if user:
                    if user.telegram_chat_id:
                        status_text = f"✅ <b>Статус уведомлений</b>\n\n👤 Пользователь: <b>{user.username}</b>\n📱 Telegram: <b>@{username}</b>\n🆔 Chat ID: <b>{user.telegram_chat_id}</b>\n📊 Статус: <b>Настроено</b>\n\n🎯 Вы будете получать уведомления о продажах ваших товаров!"
                    else:
                        status_text = f"⚠️ <b>Статус уведомлений</b>\n\n👤 Пользователь: <b>{user.username}</b>\n📱 Telegram: <b>@{username}</b>\n📊 Статус: <b>Не настроено</b>\n\n🔧 <b>Чтобы настроить:</b>\nОтправьте команду <b>/start</b>"
                    send_telegram_message(status_text, chat_id)
                else:
                    not_found_text = f"❌ <b>Пользователь не найден</b>\n\nВаш Telegram username: <b>@{username}</b>\n\n🔧 <b>Чтобы получать уведомления:</b>\n1. Зайдите на сайт <b>Nexus Dark</b>\n2. Войдите в свой аккаунт\n3. Перейдите в <b>Профиль</b>\n4. Укажите ваш Telegram username: <b>{username}</b>\n5. Сохраните изменения\n6. Отправьте <b>/start</b>"
                    send_telegram_message(not_found_text, chat_id)
            else:
                no_username_text = "❌ <b>У вас не указан Telegram username</b>\n\n🔧 <b>Чтобы получать уведомления:</b>\n1. Зайдите в <b>настройки Telegram</b>\n2. Установите <b>username</b>\n3. Зайдите на сайт <b>Nexus Dark</b>\n4. Укажите username в <b>профиле</b>\n5. Отправьте <b>/start</b>"
                send_telegram_message(no_username_text, chat_id)
        
        return jsonify({'ok': True})
    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({'ok': True})

@app.route('/telegram/manual-setup', methods=['POST'])
@login_required
def manual_telegram_setup():
    """Ручная настройка Telegram уведомлений для тестирования"""
    try:
        data = request.get_json()
        chat_id = data.get('chat_id')
        
        if not chat_id:
            return jsonify({'success': False, 'message': 'Не указан chat_id'})
        
        # Сохраняем chat_id для текущего пользователя
        current_user.telegram_chat_id = chat_id
        db.session.commit()
        
        print(f"✅ Manual setup: User {current_user.username} chat_id set to {chat_id}")
        
        # Отправляем тестовое сообщение
        test_message = f"🎉 <b>Уведомления настроены!</b>\n\nПривет, {current_user.username}!\n\nТеперь вы будете получать уведомления о продажах ваших товаров в Nexus Dark!"
        send_telegram_message(test_message, chat_id)
        
        return jsonify({
            'success': True, 
            'message': 'Уведомления настроены успешно!',
            'chat_id': chat_id
        })
        
    except Exception as e:
        print(f"❌ Manual setup error: {e}")
        return jsonify({'success': False, 'message': f'Ошибка: {str(e)}'})


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.route('/admin/user/<int:user_id>/setup_telegram', methods=['POST'])
@login_required
def setup_telegram(user_id):
    """Настройка Telegram chat_id для пользователя"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Доступ запрещен'})
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'Пользователь не найден'})
    
    data = request.get_json()
    chat_id = data.get('chat_id')
    
    if not chat_id:
        return jsonify({'success': False, 'message': 'Chat ID не указан'})
    
    try:
        user.telegram_chat_id = chat_id
        db.session.commit()
        
        # Отправляем тестовое сообщение
        test_message = f"Привет, {user.username}! 🎉\n\nTelegram уведомления настроены администратором. Теперь вы будете получать уведомления о продажах ваших товаров!"
        send_telegram_message(test_message, chat_id)
        
        return jsonify({'success': True, 'message': f'Telegram настроен для пользователя {user.username}'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Ошибка настройки: {str(e)}'})

@app.route('/telegram/test', methods=['POST'])
@login_required
def test_telegram():
    """Отправляет тестовое сообщение в Telegram"""
    if not current_user.telegram_chat_id:
        return jsonify({'success': False, 'message': 'Telegram не настроен'})
    
    test_message = f"🧪 <b>Тестовое сообщение</b>\n\n👤 Пользователь: <b>{current_user.username}</b>\n🆔 Chat ID: <b>{current_user.telegram_chat_id}</b>\n\n✅ <b>Telegram уведомления работают!</b>\n\nВы будете получать уведомления о продажах ваших товаров в Nexus Dark."
    
    try:
        send_telegram_message(test_message, current_user.telegram_chat_id)
        return jsonify({'success': True, 'message': 'Тестовое сообщение отправлено'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Ошибка отправки: {str(e)}'})

@app.route('/admin/database')
@login_required
def view_database():
    """Просмотр базы данных пользователей (только для админа)"""
    if not current_user.is_admin:
        return "Доступ запрещен", 403
    
    try:
        # Получаем всех пользователей
        users = User.query.all()
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>База данных пользователей</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background: #1a1a1a; color: #fff; }
                table { border-collapse: collapse; width: 100%; background: #2a2a2a; }
                th, td { border: 1px solid #444; padding: 8px; text-align: left; }
                th { background: #333; }
                .status { padding: 4px 8px; border-radius: 4px; }
                .configured { background: #4CAF50; color: white; }
                .pending { background: #FF9800; color: white; }
                .admin { background: #2196F3; color: white; }
                .banned { background: #f44336; color: white; }
            </style>
        </head>
        <body>
            <h1>🗄️ База данных пользователей</h1>
            <p>Всего пользователей: <strong>{}</strong></p>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Balance</th>
                    <th>Telegram</th>
                    <th>Status</th>
                    <th>Created</th>
                </tr>
        """.format(len(users))
        
        for user in users:
            # Определяем статус
            status_class = ""
            status_text = "User"
            
            if user.is_admin:
                status_class = "admin"
                status_text = "Admin"
            elif user.is_banned:
                status_class = "banned"
                status_text = "Banned"
            
            # Статус Telegram
            telegram_status = ""
            if user.telegram_chat_id:
                telegram_status = f'<span class="status configured">Настроен</span><br><small>ID: {user.telegram_chat_id}</small>'
            else:
                telegram_status = '<span class="status pending">Не настроен</span>'
            
            html += f"""
                <tr>
                    <td>{user.id}</td>
                    <td>{user.username}</td>
                    <td>{user.email}</td>
                    <td>{user.balance:.2f}₽</td>
                    <td>{telegram_status}</td>
                    <td><span class="status {status_class}">{status_text}</span></td>
                    <td>{user.created_at.strftime('%d.%m.%Y %H:%M') if user.created_at else 'N/A'}</td>
                </tr>
            """
        
        html += """
            </table>
            <br>
            <a href="/admin" style="color: #4CAF50;">← Назад к админ панели</a>
        </body>
        </html>
        """
        
        return html
        
    except Exception as e:
        return f"Ошибка: {str(e)}", 500

@app.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    """Удаление пользователя"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Доступ запрещен'})
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'Пользователь не найден'})
    
    if user.id == current_user.id:
        return jsonify({'success': False, 'message': 'Нельзя удалить самого себя'})
    
    try:
        # Удаляем все товары пользователя
        products = Product.query.filter_by(seller_id=user.id).all()
        for product in products:
            # Удаляем изображения товаров
            if product.image:
                try:
                    img_path = os.path.join(app.config['UPLOAD_FOLDER'], product.image)
                    if os.path.exists(img_path):
                        os.remove(img_path)
                except Exception:
                    pass
            db.session.delete(product)
        
        # Удаляем все товары из корзины пользователя
        cart_items = CartItem.query.filter_by(user_id=user.id).all()
        for item in cart_items:
            db.session.delete(item)
        
        # Отправляем уведомление админу об удалении
        admin_message = f"🗑️ <b>Пользователь удален</b>\n\nПользователь: <b>{user.username}</b>\nEmail: {user.email}\nTelegram: @{user.telegram_username or 'Не указан'}\nТоваров удалено: {len(products)}"
        send_admin_notification(admin_message)
        
        # Удаляем пользователя
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'success': True, 'message': f'Пользователь {user.username} удален'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Ошибка удаления: {str(e)}'})

# === 7. Запуск приложения ===
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        ensure_schema()
        if User.query.count() == 0:
            admin = User(
                username='Rodeos',
                email='rodeos@nexus.dark',
                password_hash=generate_password_hash('Rodeos24102007'),
                balance=10000.0,
                is_admin=True,
                is_banned=False,
                telegram_chat_id='1172834372'  # ID для отправки кодов
            )
            db.session.add(admin)
            db.session.commit()
            print('Создан администратор: Rodeos/Rodeos24102007')
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
