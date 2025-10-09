import requests
import json
from app import app, db, User, Product, CartItem
from datetime import datetime

# Конфигурация бота
TELEGRAM_BOT_TOKEN = '8458514538:AAFIAT7BrKelIHie9-JscBnOlAFd_V2qyMY'
ADMIN_CHAT_ID = '1172834372'
BASE_URL = 'https://api.telegram.org/bot'

def send_telegram_message(text, chat_id):
    """Отправляет сообщение в Telegram"""
    try:
        url = f"{BASE_URL}{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, data=payload, timeout=5)
        return response.json()
    except Exception as e:
        print(f"Telegram send error: {e}")
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

def handle_admin_command(message_text, chat_id):
    """Обрабатывает админ команды"""
    if chat_id != ADMIN_CHAT_ID:
        return "❌ Доступ запрещен"
    
    # Если команда не начинается с /, добавляем /
    if not message_text.startswith('/'):
        message_text = '/' + message_text
    
    parts = message_text.split()
    command = parts[0].lower()
    
    if command == '/stats':
        stats = get_user_stats()
        return f"""📊 <b>Статистика системы</b>

👥 Пользователи:
• Всего: {stats['total_users']}
• Админов: {stats['admins']}
• Заблокированных: {stats['banned']}
• Активных: {stats['active']}

📦 Товары: {stats['total_products']}"""

    elif command == '/users':
        users = get_user_list()
        if not users:
            return "❌ Пользователи не найдены"
        
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
        
        return text

    elif command == '/ban' and len(parts) > 1:
        try:
            user_id = int(parts[1])
            return ban_user(user_id)
        except ValueError:
            return "❌ Неверный ID пользователя"

    elif command == '/unban' and len(parts) > 1:
        try:
            user_id = int(parts[1])
            return unban_user(user_id)
        except ValueError:
            return "❌ Неверный ID пользователя"

    elif command == '/admin' and len(parts) > 1:
        try:
            user_id = int(parts[1])
            return make_admin(user_id)
        except ValueError:
            return "❌ Неверный ID пользователя"

    elif command == '/remove_admin' and len(parts) > 1:
        try:
            user_id = int(parts[1])
            return remove_admin(user_id)
        except ValueError:
            return "❌ Неверный ID пользователя"

    elif command == '/setup_telegram' and len(parts) > 2:
        try:
            user_id = int(parts[1])
            chat_id = parts[2]
            return setup_telegram_chat(user_id, chat_id)
        except ValueError:
            return "❌ Неверные параметры"

    elif command == '/delete' and len(parts) > 1:
        try:
            user_id = int(parts[1])
            return delete_user_admin(user_id)
        except ValueError:
            return "❌ Неверный ID пользователя"

    elif command == '/help':
        return """🔧 <b>Админ команды</b>

📊 <b>Статистика:</b>
/stats - Статистика системы

👥 <b>Пользователи:</b>
/users - Список пользователей
/ban [ID] - Заблокировать пользователя
/unban [ID] - Разблокировать пользователя
/admin [ID] - Сделать админом
/remove_admin [ID] - Убрать права админа
/delete [ID] - Удалить пользователя

📱 <b>Telegram:</b>
/setup_telegram [ID] [chat_id] - Настроить Telegram

❓ <b>Помощь:</b>
/help - Показать эту справку"""

    else:
        return "❌ Неизвестная команда. Используйте /help для справки"

def process_telegram_update(update):
    """Обрабатывает обновление от Telegram"""
    if 'message' not in update:
        return
    
    message = update['message']
    chat_id = str(message['chat']['id'])
    text = message.get('text', '')
    
    # Обрабатываем только админ команды
    if text.startswith('/'):
        response = handle_admin_command(text, chat_id)
        send_telegram_message(response, chat_id)

if __name__ == "__main__":
    print("🤖 Telegram бот запущен!")
    print("📱 Админ chat_id:", ADMIN_CHAT_ID)
    print("🔧 Доступные команды: /help")

