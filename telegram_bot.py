import requests
import json
import os
import random
import string
from app import app, db, User, Product, CartItem
from datetime import datetime

# Конфигурация бота
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8458514538:AAFIAT7BrKelIHie9-JscBnOlAFd_V2qyMY')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID', '1172834372')
BASE_URL = 'https://api.telegram.org/bot'

def create_inline_keyboard(buttons):
    """Создает inline клавиатуру с кнопками"""
    keyboard = []
    for row in buttons:
        keyboard_row = []
        for button in row:
            keyboard_row.append({
                'text': button['text'],
                'callback_data': button['callback_data']
            })
        keyboard.append(keyboard_row)
    return {'inline_keyboard': keyboard}

def send_telegram_message(text, chat_id, keyboard=None):
    """Отправляет сообщение в Telegram с возможностью добавления клавиатуры"""
    try:
        url = f"{BASE_URL}{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        
        if keyboard:
            payload['reply_markup'] = json.dumps(keyboard)
        
        response = requests.post(url, data=payload, timeout=5)
        return response.json()
    except Exception as e:
        print(f"Telegram send error: {e}")
        return None

def edit_telegram_message(text, chat_id, message_id, keyboard=None):
    """Редактирует сообщение в Telegram"""
    try:
        url = f"{BASE_URL}{TELEGRAM_BOT_TOKEN}/editMessageText"
        payload = {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        
        if keyboard:
            payload['reply_markup'] = json.dumps(keyboard)
        
        response = requests.post(url, data=payload, timeout=5)
        return response.json()
    except Exception as e:
        print(f"Telegram edit error: {e}")
        return None

def answer_callback_query(callback_query_id, text=None):
    """Отвечает на callback query"""
    try:
        url = f"{BASE_URL}{TELEGRAM_BOT_TOKEN}/answerCallbackQuery"
        payload = {
            'callback_query_id': callback_query_id
        }
        
        if text:
            payload['text'] = text
        
        response = requests.post(url, data=payload, timeout=5)
        return response.json()
    except Exception as e:
        print(f"Telegram callback answer error: {e}")
        return None

def get_user_stats():
    """Получает статистику пользователей"""
    with app.app_context():
        total_users = User.query.count()
        admins = User.query.filter_by(is_admin=True).count()
        banned = User.query.filter_by(is_banned=True).count()
        active = total_users - banned
        total_products = Product.query.count()
        
        return {
            'total_users': total_users,
            'admins': admins,
            'banned': banned,
            'active': active,
            'total_products': total_products
        }

def get_user_list():
    """Получает список пользователей"""
    with app.app_context():
        users = User.query.all()
        user_list = []
        
        for user in users:
            status = []
            if user.is_admin:
                status.append("👑 Админ")
            if user.is_banned:
                status.append("🚫 Заблокирован")
            if not user.is_banned:
                status.append("✅ Активен")
            
            telegram_status = "📱 Настроен" if user.telegram_chat_id else "⚠️ Не настроен"
            
            user_list.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'balance': user.balance,
                'status': " | ".join(status),
                'telegram': f"@{user.telegram_username}" if user.telegram_username else "Не указан",
                'telegram_status': telegram_status,
                'created_at': user.created_at.strftime('%d.%m.%Y')
            })
        
        return user_list

def get_user_by_username(username):
    """Находит пользователя по имени"""
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        return user

def get_user_management_buttons():
    """Возвращает кнопки управления пользователями с именами"""
    with app.app_context():
        users = User.query.limit(10).all()  # Берем первых 10 пользователей
        buttons = []
        
        # Добавляем кнопки для каждого пользователя
        for user in users:
            status_icon = "👑" if user.is_admin else "🚫" if user.is_banned else "✅"
            username = user.username[:15] + "..." if len(user.username) > 15 else user.username
            
            buttons.append([
                {
                    'text': f"{status_icon} {username}",
                    'callback_data': f"user_info_{user.id}"
                }
            ])
        
        # Добавляем кнопки управления
        buttons.append([
            {'text': '🔍 Найти по имени', 'callback_data': 'find_user'},
            {'text': '📝 Ввести команду', 'callback_data': 'enter_command'}
        ])
        
        buttons.append([
            {'text': '🔙 Назад', 'callback_data': 'main_menu'}
        ])
        
        return create_inline_keyboard(buttons)

def ban_user(user_id):
    """Блокирует пользователя"""
    with app.app_context():
        user = User.query.get(user_id)
        if user:
            user.is_banned = True
            db.session.commit()
            return f"✅ Пользователь {user.username} заблокирован"
        return "❌ Пользователь не найден"

def ban_user_by_username(username):
    """Блокирует пользователя по имени"""
    with app.app_context():
        user = get_user_by_username(username)
        if user:
            user.is_banned = True
            db.session.commit()
            return f"✅ Пользователь {user.username} заблокирован"
        return f"❌ Пользователь '{username}' не найден"

def unban_user(user_id):
    """Разблокирует пользователя"""
    with app.app_context():
        user = User.query.get(user_id)
        if user:
            user.is_banned = False
            db.session.commit()
            return f"✅ Пользователь {user.username} разблокирован"
        return "❌ Пользователь не найден"

def unban_user_by_username(username):
    """Разблокирует пользователя по имени"""
    with app.app_context():
        user = get_user_by_username(username)
        if user:
            user.is_banned = False
            db.session.commit()
            return f"✅ Пользователь {user.username} разблокирован"
        return f"❌ Пользователь '{username}' не найден"

def make_admin(user_id):
    """Делает пользователя админом"""
    with app.app_context():
        user = User.query.get(user_id)
        if user:
            user.is_admin = True
            db.session.commit()
            return f"✅ Пользователь {user.username} назначен админом"
        return "❌ Пользователь не найден"

def make_admin_by_username(username):
    """Делает пользователя админом по имени"""
    with app.app_context():
        user = get_user_by_username(username)
        if user:
            user.is_admin = True
            db.session.commit()
            return f"✅ Пользователь {user.username} назначен админом"
        return f"❌ Пользователь '{username}' не найден"

def remove_admin(user_id):
    """Убирает права админа"""
    with app.app_context():
        user = User.query.get(user_id)
        if user:
            user.is_admin = False
            db.session.commit()
            return f"✅ У пользователя {user.username} убраны права админа"
        return "❌ Пользователь не найден"

def remove_admin_by_username(username):
    """Убирает права админа по имени"""
    with app.app_context():
        user = get_user_by_username(username)
        if user:
            user.is_admin = False
            db.session.commit()
            return f"✅ У пользователя {user.username} убраны права админа"
        return f"❌ Пользователь '{username}' не найден"

def setup_telegram_chat(user_id, chat_id):
    """Настраивает Telegram chat_id для пользователя"""
    with app.app_context():
        user = User.query.get(user_id)
        if user:
            user.telegram_chat_id = chat_id
            db.session.commit()
            return f"✅ Telegram настроен для пользователя {user.username}"
        return "❌ Пользователь не найден"

def delete_user_admin(user_id):
    """Удаляет пользователя"""
    with app.app_context():
        user = User.query.get(user_id)
        if user:
            username = user.username
            
            # Удаляем все товары пользователя
            products = Product.query.filter_by(seller_id=user.id).all()
            for product in products:
                db.session.delete(product)
            
            # Удаляем все товары из корзины пользователя
            cart_items = CartItem.query.filter_by(user_id=user.id).all()
            for item in cart_items:
                db.session.delete(item)
            
            # Удаляем пользователя
            db.session.delete(user)
            db.session.commit()
            
            return f"✅ Пользователь {username} удален (товаров: {len(products)})"
        return "❌ Пользователь не найден"

def change_admin_username(new_username):
    """Изменяет логин админа"""
    with app.app_context():
        # Находим админа (предполагаем, что это пользователь с ID 1 или первый админ)
        admin = User.query.filter_by(is_admin=True).first()
        if admin:
            old_username = admin.username
            admin.username = new_username
            db.session.commit()
            return f"✅ Логин админа изменен с '{old_username}' на '{new_username}'"
        return "❌ Админ не найден"

def change_admin_password(new_password):
    """Изменяет пароль админа"""
    with app.app_context():
        from werkzeug.security import generate_password_hash
        
        # Находим админа
        admin = User.query.filter_by(is_admin=True).first()
        if admin:
            admin.password_hash = generate_password_hash(new_password)
            db.session.commit()
            return f"✅ Пароль админа изменен"
        return "❌ Админ не найден"

def get_admin_info():
    """Получает информацию об админе"""
    with app.app_context():
        admin = User.query.filter_by(is_admin=True).first()
        if admin:
            return {
                'username': admin.username,
                'email': admin.email,
                'created_at': admin.created_at.strftime('%d.%m.%Y %H:%M'),
                'telegram_chat_id': admin.telegram_chat_id,
                'is_banned': admin.is_banned
            }
        return None

def generate_random_username():
    """Генерирует случайный логин"""
    adjectives = ['super', 'mega', 'ultra', 'pro', 'master', 'elite', 'prime', 'vip']
    nouns = ['admin', 'user', 'boss', 'chief', 'leader', 'king', 'lord', 'hero']
    numbers = random.randint(100, 999)
    
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    
    return f"{adjective}{noun}{numbers}"

def generate_random_password():
    """Генерирует случайный пароль"""
    length = 12
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def get_main_menu():
    """Возвращает главное меню с кнопками"""
    buttons = [
        [
            {'text': '📊 Статистика', 'callback_data': 'stats'},
            {'text': '👥 Пользователи', 'callback_data': 'users'}
        ],
        [
            {'text': '🔧 Управление', 'callback_data': 'management'},
            {'text': '📱 Telegram', 'callback_data': 'telegram'}
        ],
        [
            {'text': '⚙️ Настройки админа', 'callback_data': 'admin_settings'}
        ],
        [
            {'text': '❓ Помощь', 'callback_data': 'help'}
        ]
    ]
    return create_inline_keyboard(buttons)

def get_management_menu():
    """Возвращает меню управления пользователями"""
    buttons = [
        [
            {'text': '👥 Выбрать пользователя', 'callback_data': 'select_user'},
            {'text': '🔍 Найти по имени', 'callback_data': 'find_user'}
        ],
        [
            {'text': '📝 Ввести команду', 'callback_data': 'enter_command'}
        ],
        [
            {'text': '🔙 Назад', 'callback_data': 'main_menu'}
        ]
    ]
    return create_inline_keyboard(buttons)

def get_user_actions_menu(user_id):
    """Возвращает меню действий для конкретного пользователя"""
    with app.app_context():
        user = User.query.get(user_id)
        if not user:
            return None
        
        buttons = [
            [
                {'text': f'👤 {user.username}', 'callback_data': f'user_info_{user_id}'}
            ],
            [
                {'text': '🚫 Заблокировать', 'callback_data': f'ban_user_{user_id}'},
                {'text': '✅ Разблокировать', 'callback_data': f'unban_user_{user_id}'}
            ],
            [
                {'text': '👑 Сделать админом', 'callback_data': f'make_admin_{user_id}'},
                {'text': '👤 Убрать админа', 'callback_data': f'remove_admin_{user_id}'}
            ],
            [
                {'text': '🗑️ Удалить', 'callback_data': f'delete_user_{user_id}'}
            ],
            [
                {'text': '🔙 Назад к списку', 'callback_data': 'management'}
            ]
        ]
        return create_inline_keyboard(buttons)

def get_telegram_menu():
    """Возвращает меню настроек Telegram"""
    buttons = [
        [
            {'text': '📱 Настроить Telegram', 'callback_data': 'setup_telegram'}
        ],
        [
            {'text': '🔙 Назад', 'callback_data': 'main_menu'}
        ]
    ]
    return create_inline_keyboard(buttons)

def get_admin_settings_menu():
    """Возвращает меню настроек админа"""
    buttons = [
        [
            {'text': '👤 Изменить логин', 'callback_data': 'admin_username_menu'},
            {'text': '🔒 Изменить пароль', 'callback_data': 'admin_password_menu'}
        ],
        [
            {'text': 'ℹ️ Информация об админе', 'callback_data': 'admin_info'}
        ],
        [
            {'text': '🔙 Назад', 'callback_data': 'main_menu'}
        ]
    ]
    return create_inline_keyboard(buttons)

def get_admin_username_menu():
    """Возвращает меню изменения логина админа"""
    buttons = [
        [
            {'text': '🎲 Сгенерировать случайный', 'callback_data': 'generate_random_username'},
            {'text': '📝 Ввести вручную', 'callback_data': 'enter_username_manual'}
        ],
        [
            {'text': '🔙 Назад к настройкам', 'callback_data': 'admin_settings'}
        ]
    ]
    return create_inline_keyboard(buttons)

def get_admin_password_menu():
    """Возвращает меню изменения пароля админа"""
    buttons = [
        [
            {'text': '🎲 Сгенерировать случайный', 'callback_data': 'generate_random_password'},
            {'text': '📝 Ввести вручную', 'callback_data': 'enter_password_manual'}
        ],
        [
            {'text': '🔙 Назад к настройкам', 'callback_data': 'admin_settings'}
        ]
    ]
    return create_inline_keyboard(buttons)

def handle_admin_command(message_text, chat_id):
    """Обрабатывает админ команды"""
    if chat_id != ADMIN_CHAT_ID:
        return "❌ Доступ запрещен", None
    
    # Если команда не начинается с /, добавляем /
    if not message_text.startswith('/'):
        message_text = '/' + message_text
    
    parts = message_text.split()
    command = parts[0].lower()
    
    if command == '/start' or command == '/menu':
        return "🔧 <b>Админ панель</b>\n\nВыберите действие:", get_main_menu()
    
    elif command == '/stats':
        stats = get_user_stats()
        text = f"""📊 <b>Статистика системы</b>

👥 Пользователи:
• Всего: {stats['total_users']}
• Админов: {stats['admins']}
• Заблокированных: {stats['banned']}
• Активных: {stats['active']}

📦 Товары: {stats['total_products']}"""
        return text, get_main_menu()

    elif command == '/users':
        users = get_user_list()
        if not users:
            return "❌ Пользователи не найдены", get_main_menu()
        
        text = "👥 <b>Список пользователей</b>\n\n"
        for user in users[:10]:  # Показываем первых 10
            text += f"<b>{user['username']}</b> (ID: {user['id']})\n"
            text += f"📧 {user['email']}\n"
            text += f"💰 Баланс: {user['balance']}₽\n"
            text += f"📱 Telegram: {user['telegram']} ({user['telegram_status']})\n"
            text += f"📅 Регистрация: {user['created_at']}\n"
            text += f"🔹 {user['status']}\n\n"
        
        if len(users) > 10:
            text += f"... и еще {len(users) - 10} пользователей"
        
        return text, get_main_menu()

    elif command == '/ban' and len(parts) > 1:
        try:
            user_id = int(parts[1])
            return ban_user(user_id), get_main_menu()
        except ValueError:
            return "❌ Неверный ID пользователя", get_main_menu()

    elif command == '/unban' and len(parts) > 1:
        try:
            user_id = int(parts[1])
            return unban_user(user_id), get_main_menu()
        except ValueError:
            return "❌ Неверный ID пользователя", get_main_menu()

    elif command == '/admin' and len(parts) > 1:
        try:
            user_id = int(parts[1])
            return make_admin(user_id), get_main_menu()
        except ValueError:
            return "❌ Неверный ID пользователя", get_main_menu()

    elif command == '/remove_admin' and len(parts) > 1:
        try:
            user_id = int(parts[1])
            return remove_admin(user_id), get_main_menu()
        except ValueError:
            return "❌ Неверный ID пользователя", get_main_menu()

    elif command == '/setup_telegram' and len(parts) > 2:
        try:
            user_id = int(parts[1])
            chat_id = parts[2]
            return setup_telegram_chat(user_id, chat_id), get_main_menu()
        except ValueError:
            return "❌ Неверные параметры", get_main_menu()

    elif command == '/delete' and len(parts) > 1:
        try:
            user_id = int(parts[1])
            return delete_user_admin(user_id), get_main_menu()
        except ValueError:
            return "❌ Неверный ID пользователя", get_main_menu()

    elif command == '/help':
        text = """🔧 <b>Админ панель</b>

Используйте кнопки для навигации по меню.

📊 <b>Статистика:</b>
Показывает общую статистику системы

👥 <b>Пользователи:</b>
Просмотр списка всех пользователей

🔧 <b>Управление:</b>
• Заблокировать/разблокировать пользователей
• Назначить/убрать права админа
• Удалить пользователей

📱 <b>Telegram:</b>
Настройка Telegram для пользователей

❓ <b>Помощь:</b>
Показать эту справку"""
        return text, get_main_menu()

    else:
        return "❌ Неизвестная команда. Используйте /start для главного меню", get_main_menu()

def handle_callback_query(callback_query, chat_id):
    """Обрабатывает нажатия на кнопки"""
    if chat_id != ADMIN_CHAT_ID:
        return "❌ Доступ запрещен", None
    
    callback_data = callback_query['data']
    message_id = callback_query['message']['message_id']
    
    if callback_data == 'main_menu':
        return "🔧 <b>Админ панель</b>\n\nВыберите действие:", get_main_menu()
    
    elif callback_data == 'stats':
        stats = get_user_stats()
        text = f"""📊 <b>Статистика системы</b>

👥 Пользователи:
• Всего: {stats['total_users']}
• Админов: {stats['admins']}
• Заблокированных: {stats['banned']}
• Активных: {stats['active']}

📦 Товары: {stats['total_products']}"""
        return text, get_main_menu()
    
    elif callback_data == 'users':
        users = get_user_list()
        if not users:
            return "❌ Пользователи не найдены", get_main_menu()
        
        text = "👥 <b>Список пользователей</b>\n\n"
        for user in users[:10]:  # Показываем первых 10
            text += f"<b>{user['username']}</b> (ID: {user['id']})\n"
            text += f"📧 {user['email']}\n"
            text += f"💰 Баланс: {user['balance']}₽\n"
            text += f"📱 Telegram: {user['telegram']} ({user['telegram_status']})\n"
            text += f"📅 Регистрация: {user['created_at']}\n"
            text += f"🔹 {user['status']}\n\n"
        
        if len(users) > 10:
            text += f"... и еще {len(users) - 10} пользователей"
        
        return text, get_main_menu()
    
    elif callback_data == 'management':
        return "🔧 <b>Управление пользователями</b>\n\nВыберите действие:", get_management_menu()
    
    elif callback_data == 'select_user':
        return "👥 <b>Выберите пользователя</b>\n\nНажмите на пользователя для управления:", get_user_management_buttons()
    
    elif callback_data == 'find_user':
        return "🔍 <b>Поиск пользователя</b>\n\nВведите имя пользователя для поиска:\n\n<code>find username</code>\n\nНапример: <code>find admin</code>", get_management_menu()
    
    elif callback_data == 'enter_command':
        return "📝 <b>Ввод команды</b>\n\nДоступные команды:\n\n<code>ban username</code> - заблокировать\n<code>unban username</code> - разблокировать\n<code>admin username</code> - сделать админом\n<code>remove_admin username</code> - убрать админа\n<code>delete username</code> - удалить\n\nНапример: <code>ban testuser</code>", get_management_menu()
    
    elif callback_data.startswith('user_info_'):
        user_id = int(callback_data.split('_')[2])
        with app.app_context():
            user = User.query.get(user_id)
            if user:
                status = []
                if user.is_admin:
                    status.append("👑 Админ")
                if user.is_banned:
                    status.append("🚫 Заблокирован")
                if not user.is_banned:
                    status.append("✅ Активен")
                
                telegram_status = "📱 Настроен" if user.telegram_chat_id else "⚠️ Не настроен"
                
                text = f"""👤 <b>Информация о пользователе</b>

<b>Имя:</b> {user.username}
<b>Email:</b> {user.email}
<b>ID:</b> {user.id}
<b>Баланс:</b> {user.balance}₽
<b>Telegram:</b> {f'@{user.telegram_username}' if user.telegram_username else 'Не указан'} ({telegram_status})
<b>Статус:</b> {" | ".join(status)}
<b>Регистрация:</b> {user.created_at.strftime('%d.%m.%Y %H:%M')}

<b>💡 Скопируйте имя:</b> <code>{user.username}</code>"""
                
                return text, get_user_actions_menu(user_id)
            else:
                return "❌ Пользователь не найден", get_management_menu()
    
    elif callback_data.startswith('ban_user_'):
        user_id = int(callback_data.split('_')[2])
        result = ban_user(user_id)
        return result, get_management_menu()
    
    elif callback_data.startswith('unban_user_'):
        user_id = int(callback_data.split('_')[2])
        result = unban_user(user_id)
        return result, get_management_menu()
    
    elif callback_data.startswith('make_admin_'):
        user_id = int(callback_data.split('_')[2])
        result = make_admin(user_id)
        return result, get_management_menu()
    
    elif callback_data.startswith('remove_admin_'):
        user_id = int(callback_data.split('_')[2])
        result = remove_admin(user_id)
        return result, get_management_menu()
    
    elif callback_data.startswith('delete_user_'):
        user_id = int(callback_data.split('_')[2])
        result = delete_user_admin(user_id)
        return result, get_management_menu()
    
    elif callback_data == 'telegram':
        return "📱 <b>Настройки Telegram</b>\n\nВыберите действие:", get_telegram_menu()
    
    elif callback_data == 'admin_settings':
        return "⚙️ <b>Настройки админа</b>\n\nВыберите действие:", get_admin_settings_menu()
    
    elif callback_data == 'admin_username_menu':
        return "👤 <b>Изменение логина админа</b>\n\nВыберите способ изменения логина:", get_admin_username_menu()
    
    elif callback_data == 'admin_password_menu':
        return "🔒 <b>Изменение пароля админа</b>\n\nВыберите способ изменения пароля:", get_admin_password_menu()
    
    elif callback_data == 'generate_random_username':
        new_username = generate_random_username()
        result = change_admin_username(new_username)
        text = f"{result}\n\n<b>💡 Новый логин:</b> <code>{new_username}</code>\n\n<b>⚠️ Сохраните логин!</b>"
        return text, get_admin_settings_menu()
    
    elif callback_data == 'generate_random_password':
        new_password = generate_random_password()
        result = change_admin_password(new_password)
        text = f"{result}\n\n<b>💡 Новый пароль:</b> <code>{new_password}</code>\n\n<b>⚠️ Сохраните пароль!</b>"
        return text, get_admin_settings_menu()
    
    elif callback_data == 'enter_username_manual':
        return "📝 <b>Ввод логина вручную</b>\n\nВведите новый логин в формате:\n\n<code>change_username новый_логин</code>\n\nНапример: <code>change_username newadmin</code>", get_admin_username_menu()
    
    elif callback_data == 'enter_password_manual':
        return "📝 <b>Ввод пароля вручную</b>\n\nВведите новый пароль в формате:\n\n<code>change_password новый_пароль</code>\n\nНапример: <code>change_password newpassword123</code>", get_admin_password_menu()
    
    elif callback_data == 'admin_info':
        admin_info = get_admin_info()
        if admin_info:
            text = f"""ℹ️ <b>Информация об админе</b>

<b>Логин:</b> {admin_info['username']}
<b>Email:</b> {admin_info['email']}
<b>Telegram Chat ID:</b> {admin_info['telegram_chat_id'] or 'Не настроен'}
<b>Статус:</b> {'🚫 Заблокирован' if admin_info['is_banned'] else '✅ Активен'}
<b>Создан:</b> {admin_info['created_at']}

<b>💡 Скопируйте логин:</b> <code>{admin_info['username']}</code>"""
            return text, get_admin_settings_menu()
        else:
            return "❌ Информация об админе не найдена", get_admin_settings_menu()
    
    elif callback_data == 'help':
        text = """🔧 <b>Админ панель</b>

Используйте кнопки для навигации по меню.

📊 <b>Статистика:</b>
Показывает общую статистику системы

👥 <b>Пользователи:</b>
Просмотр списка всех пользователей

🔧 <b>Управление:</b>
• Выберите пользователя из списка
• Найдите пользователя по имени
• Управление через кнопки

📱 <b>Telegram:</b>
Настройка Telegram для пользователей

⚙️ <b>Настройки админа:</b>
• Изменение логина админа (случайный или вручную)
• Изменение пароля админа (случайный или вручную)
• Информация об админе

❓ <b>Помощь:</b>
Показать эту справку

<b>💡 Все действия выполняются через кнопки!</b>
Никаких команд вводить не нужно."""
        return text, get_main_menu()
    
    else:
        return "❌ Неизвестное действие", get_main_menu()

def process_telegram_update(update):
    """Обрабатывает обновление от Telegram"""
    # Обработка callback_query (нажатия на кнопки)
    if 'callback_query' in update:
        callback_query = update['callback_query']
        chat_id = str(callback_query['message']['chat']['id'])
        message_id = callback_query['message']['message_id']
        
        text, keyboard = handle_callback_query(callback_query, chat_id)
        
        # Отвечаем на callback query
        answer_callback_query(callback_query['id'])
        
        # Редактируем сообщение
        edit_telegram_message(text, chat_id, message_id, keyboard)
        return
    
    # Обработка обычных сообщений
    if 'message' not in update:
        return
    
    message = update['message']
    chat_id = str(message['chat']['id'])
    text = message.get('text', '')
    
    # Обрабатываем команды и сообщения
    if text.startswith('/') or text in ['start', 'menu', 'help']:
        response_text, keyboard = handle_admin_command(text, chat_id)
        send_telegram_message(response_text, chat_id, keyboard)
    else:
        # Обработка специальных команд управления пользователями
        parts = text.split()
        if len(parts) >= 2:
            action = parts[0]
            username_or_id = parts[1]
            
            # Проверяем, является ли второй параметр числом (ID) или строкой (имя)
            try:
                user_id = int(username_or_id)
                # Это ID пользователя
                if action == 'ban_user':
                    response_text = ban_user(user_id)
                elif action == 'unban_user':
                    response_text = unban_user(user_id)
                elif action == 'make_admin':
                    response_text = make_admin(user_id)
                elif action == 'remove_admin':
                    response_text = remove_admin(user_id)
                elif action == 'delete_user':
                    response_text = delete_user_admin(user_id)
                elif action == 'setup_telegram' and len(parts) >= 3:
                    chat_id_param = parts[2]
                    response_text = setup_telegram_chat(user_id, chat_id_param)
                else:
                    response_text = "❌ Неизвестная команда"
            except ValueError:
                # Это имя пользователя
                username = username_or_id
                if action == 'ban':
                    response_text = ban_user_by_username(username)
                elif action == 'unban':
                    response_text = unban_user_by_username(username)
                elif action == 'admin':
                    response_text = make_admin_by_username(username)
                elif action == 'remove_admin':
                    response_text = remove_admin_by_username(username)
                elif action == 'delete':
                    user = get_user_by_username(username)
                    if user:
                        response_text = delete_user_admin(user.id)
                    else:
                        response_text = f"❌ Пользователь '{username}' не найден"
                elif action == 'find':
                    user = get_user_by_username(username)
                    if user:
                        status = []
                        if user.is_admin:
                            status.append("👑 Админ")
                        if user.is_banned:
                            status.append("🚫 Заблокирован")
                        if not user.is_banned:
                            status.append("✅ Активен")
                        
                        telegram_status = "📱 Настроен" if user.telegram_chat_id else "⚠️ Не настроен"
                        
                        response_text = f"""🔍 <b>Найден пользователь</b>

<b>Имя:</b> {user.username}
<b>Email:</b> {user.email}
<b>ID:</b> {user.id}
<b>Баланс:</b> {user.balance}₽
<b>Telegram:</b> {f'@{user.telegram_username}' if user.telegram_username else 'Не указан'} ({telegram_status})
<b>Статус:</b> {" | ".join(status)}
<b>Регистрация:</b> {user.created_at.strftime('%d.%m.%Y %H:%M')}

<b>💡 Скопируйте имя:</b> <code>{user.username}</code>"""
                    else:
                        response_text = f"❌ Пользователь '{username}' не найден"
                elif action == 'change_username':
                    new_username = username
                    response_text = change_admin_username(new_username)
                elif action == 'change_password':
                    new_password = username
                    response_text = change_admin_password(new_password)
                else:
                    response_text = "❌ Неизвестная команда"
            
            send_telegram_message(response_text, chat_id, get_main_menu())
        else:
            # Показываем главное меню для любых других сообщений
            send_telegram_message("🔧 <b>Админ панель</b>\n\nВыберите действие:", chat_id, get_main_menu())

if __name__ == "__main__":
    print("🤖 Telegram бот запущен!")
    print("📱 Админ chat_id:", ADMIN_CHAT_ID)
    print("🔧 Используйте /start для главного меню с кнопками")
    print("📊 Доступные функции: статистика, управление пользователями, настройки Telegram")

