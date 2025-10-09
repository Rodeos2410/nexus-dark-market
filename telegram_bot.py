import requests
import json
import os
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

def ban_user(user_id):
    """Блокирует пользователя"""
    with app.app_context():
        user = User.query.get(user_id)
        if user:
            user.is_banned = True
            db.session.commit()
            return f"✅ Пользователь {user.username} заблокирован"
        return "❌ Пользователь не найден"

def unban_user(user_id):
    """Разблокирует пользователя"""
    with app.app_context():
        user = User.query.get(user_id)
        if user:
            user.is_banned = False
            db.session.commit()
            return f"✅ Пользователь {user.username} разблокирован"
        return "❌ Пользователь не найден"

def make_admin(user_id):
    """Делает пользователя админом"""
    with app.app_context():
        user = User.query.get(user_id)
        if user:
            user.is_admin = True
            db.session.commit()
            return f"✅ Пользователь {user.username} назначен админом"
        return "❌ Пользователь не найден"

def remove_admin(user_id):
    """Убирает права админа"""
    with app.app_context():
        user = User.query.get(user_id)
        if user:
            user.is_admin = False
            db.session.commit()
            return f"✅ У пользователя {user.username} убраны права админа"
        return "❌ Пользователь не найден"

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
            {'text': '❓ Помощь', 'callback_data': 'help'}
        ]
    ]
    return create_inline_keyboard(buttons)

def get_management_menu():
    """Возвращает меню управления пользователями"""
    buttons = [
        [
            {'text': '🚫 Заблокировать', 'callback_data': 'ban_user'},
            {'text': '✅ Разблокировать', 'callback_data': 'unban_user'}
        ],
        [
            {'text': '👑 Сделать админом', 'callback_data': 'make_admin'},
            {'text': '👤 Убрать админа', 'callback_data': 'remove_admin'}
        ],
        [
            {'text': '🗑️ Удалить пользователя', 'callback_data': 'delete_user'}
        ],
        [
            {'text': '🔙 Назад', 'callback_data': 'main_menu'}
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
    
    elif callback_data == 'telegram':
        return "📱 <b>Настройки Telegram</b>\n\nВыберите действие:", get_telegram_menu()
    
    elif callback_data == 'help':
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
    
    elif callback_data in ['ban_user', 'unban_user', 'make_admin', 'remove_admin', 'delete_user', 'setup_telegram']:
        return f"⚠️ Для выполнения действия '{callback_data}' введите ID пользователя в формате:\n\n<code>{callback_data} [ID]</code>\n\nНапример: <code>ban_user 123</code>", get_main_menu()
    
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
            try:
                user_id = int(parts[1])
                
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
                
                send_telegram_message(response_text, chat_id, get_main_menu())
            except ValueError:
                send_telegram_message("❌ Неверный ID пользователя", chat_id, get_main_menu())
        else:
            # Показываем главное меню для любых других сообщений
            send_telegram_message("🔧 <b>Админ панель</b>\n\nВыберите действие:", chat_id, get_main_menu())

if __name__ == "__main__":
    print("🤖 Telegram бот запущен!")
    print("📱 Админ chat_id:", ADMIN_CHAT_ID)
    print("🔧 Используйте /start для главного меню с кнопками")
    print("📊 Доступные функции: статистика, управление пользователями, настройки Telegram")

