#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import threading
import time
import requests
import json
from datetime import datetime

# Импортируем основное приложение
from app import app, db, User, Product, CartItem

# === Конфигурация бота ===
TELEGRAM_BOT_TOKEN = '8458514538:AAFIAT7BrKelIHie9-JscBnOlAFd_V2qyMY'
ADMIN_CHAT_ID = '1172834372'
BASE_URL = 'https://api.telegram.org/bot'

def send_telegram_message(text, chat_id, reply_markup=None):
    """Отправляет сообщение в Telegram"""
    try:
        url = f"{BASE_URL}{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        if reply_markup:
            payload['reply_markup'] = json.dumps(reply_markup)
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
        result = []
        for user in users:
            result.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'balance': user.balance,
                'telegram': f"@{user.telegram_username}" if user.telegram_username else "Не указан",
                'telegram_status': "📱 Настроен" if user.telegram_chat_id else "⚠️ Не настроен",
                'created_at': user.created_at.strftime('%d.%m.%Y'),
                'status': "🚫 Заблокирован" if user.is_banned else "✅ Активен"
            })
        return result

def find_user_by_username(username):
    """Находит пользователя по имени"""
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        return user

def change_balance(user_id, amount):
    """Изменяет баланс пользователя"""
    with app.app_context():
        user = User.query.get(user_id)
        if user:
            old_balance = user.balance
            user.balance = float(amount)
            db.session.commit()
            return f"✅ Баланс пользователя {user.username} изменен с {old_balance}₽ на {amount}₽"
        return "❌ Пользователь не найден"

def ban_user(user_id):
    """Блокирует пользователя"""
    with app.app_context():
        user = User.query.get(user_id)
        if user:
            user.is_banned = True
            db.session.commit()
            return f"🚫 Пользователь {user.username} заблокирован"
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
            return f"👑 Пользователь {user.username} назначен администратором"
        return "❌ Пользователь не найден"

def remove_admin(user_id):
    """Убирает права админа"""
    with app.app_context():
        user = User.query.get(user_id)
        if user:
            user.is_admin = False
            db.session.commit()
            return f"👤 У пользователя {user.username} убраны права администратора"
        return "❌ Пользователь не найден"

def delete_user_admin(user_id):
    """Удаляет пользователя"""
    with app.app_context():
        user = User.query.get(user_id)
        if user:
            username = user.username
            db.session.delete(user)
            db.session.commit()
            return f"🗑️ Пользователь {username} удален"
        return "❌ Пользователь не найден"

def get_main_keyboard():
    """Создает основную клавиатуру"""
    return {
        'inline_keyboard': [
            [
                {'text': '📊 Статистика', 'callback_data': 'stats'},
                {'text': '👥 Пользователи', 'callback_data': 'users'}
            ],
            [
                {'text': '💰 Баланс', 'callback_data': 'balance'},
                {'text': '🔧 Управление', 'callback_data': 'management'}
            ],
            [
                {'text': '❓ Помощь', 'callback_data': 'help'}
            ]
        ]
    }

def get_balance_keyboard():
    """Создает клавиатуру управления балансом"""
    return {
        'inline_keyboard': [
            [
                {'text': '💰 Изменить баланс', 'callback_data': 'change_balance'},
                {'text': '📊 Просмотр балансов', 'callback_data': 'view_balances'}
            ],
            [
                {'text': '🔙 Назад', 'callback_data': 'main'}
            ]
        ]
    }

def get_user_actions_keyboard(user_id):
    """Создает клавиатуру действий с пользователем"""
    return {
        'inline_keyboard': [
            [
                {'text': '💰 Изменить баланс', 'callback_data': f'balance_user_{user_id}'},
                {'text': '🚫 Заблокировать', 'callback_data': f'ban_user_{user_id}'}
            ],
            [
                {'text': '✅ Разблокировать', 'callback_data': f'unban_user_{user_id}'},
                {'text': '👑 Сделать админом', 'callback_data': f'admin_user_{user_id}'}
            ],
            [
                {'text': '👤 Убрать админа', 'callback_data': f'remove_admin_user_{user_id}'},
                {'text': '🗑️ Удалить', 'callback_data': f'delete_user_{user_id}'}
            ],
            [
                {'text': '🔙 Назад', 'callback_data': 'main'}
            ]
        ]
    }

# Глобальная переменная для хранения состояния
pending_balance_change = {}

def handle_balance_change(username, amount):
    """Обрабатывает изменение баланса по имени пользователя"""
    user = find_user_by_username(username)
    if user:
        old_balance = user.balance
        user.balance = float(amount)
        db.session.commit()
        return f"✅ Баланс пользователя {user.username} изменен с {old_balance}₽ на {amount}₽"
    return "❌ Пользователь не найден"

def handle_admin_command(message_text, chat_id):
    """Обрабатывает админ команды"""
    if chat_id != ADMIN_CHAT_ID:
        return "❌ Доступ запрещен", None
    
    text = message_text.strip()
    
    # Главное меню
    if text.lower() in ['/start', '/help', 'меню', 'start', 'help']:
        return "🔧 <b>Админ панель Nexus Dark</b>\n\nВыберите действие:", get_main_keyboard()

    # Статистика
    elif text.lower() in ['статистика', 'stats', 'стат']:
        stats = get_user_stats()
        return f"""📊 <b>Статистика системы</b>

👥 Пользователи:
• Всего: {stats['total_users']}
• Админов: {stats['admins']}
• Заблокированных: {stats['banned']}
• Активных: {stats['active']}

📦 Товары: {stats['total_products']}""", get_main_keyboard()
    
    # Список пользователей
    elif text.lower() in ['пользователи', 'users', 'юзеры']:
        users = get_user_list()
        if not users:
            return "❌ Пользователи не найдены", get_main_keyboard()
        
        text_result = "👥 <b>Список пользователей</b>\n\n"
        for user in users[:10]:  # Показываем первых 10
            text_result += f"<code>{user['username']}</code> (ID: {user['id']})\n"
            text_result += f"📧 {user['email']}\n"
            text_result += f"💰 Баланс: {user['balance']}₽\n"
            text_result += f"📱 Telegram: {user['telegram']} ({user['telegram_status']})\n"
            text_result += f"📅 Регистрация: {user['created_at']}\n"
            text_result += f"🔹 {user['status']}\n\n"
        
        if len(users) > 10:
            text_result += f"... и еще {len(users) - 10} пользователей"
        
        return text_result, get_main_keyboard()

    # Проверяем, является ли сообщение числом (для изменения баланса)
    elif text.replace('.', '').replace(',', '').isdigit():
        try:
            amount = float(text.replace(',', '.'))
            # Сохраняем сумму для следующего сообщения
            pending_balance_change[chat_id] = amount
            return f"💰 <b>Изменение баланса</b>\n\nСумма: <b>{amount}₽</b>\n\nВведите имя пользователя:", get_balance_keyboard()
        except ValueError:
            return "❌ Неверная сумма", get_balance_keyboard()

    # Проверяем, является ли сообщение именем пользователя
    else:
        user = find_user_by_username(text)
        if user:
            return f"""👤 <b>Пользователь найден</b>

<b>Имя:</b> <code>{user.username}</code>
<b>Email:</b> {user.email}
<b>Баланс:</b> {user.balance}₽
<b>Статус:</b> {'🚫 Заблокирован' if user.is_banned else '✅ Активен'}
<b>Админ:</b> {'👑 Да' if user.is_admin else '👤 Нет'}
<b>Telegram:</b> {'📱 Настроен' if user.telegram_chat_id else '⚠️ Не настроен'}

Выберите действие:""", get_user_actions_keyboard(user.id)
        else:
            return f"❌ Пользователь '{text}' не найден\n\nПопробуйте:\n• Ввести точное имя пользователя\n• Посмотреть список: 'пользователи'", get_main_keyboard()

def handle_callback_query(callback_data, chat_id):
    """Обрабатывает нажатия на кнопки"""
    if chat_id != ADMIN_CHAT_ID:
        return "❌ Доступ запрещен", None
    
    if callback_data == 'main':
        return "🔧 <b>Админ панель Nexus Dark</b>\n\nВыберите действие:", get_main_keyboard()
    
    elif callback_data == 'stats':
        stats = get_user_stats()
        return f"""📊 <b>Статистика системы</b>

👥 Пользователи:
• Всего: {stats['total_users']}
• Админов: {stats['admins']}
• Заблокированных: {stats['banned']}
• Активных: {stats['active']}

📦 Товары: {stats['total_products']}""", get_main_keyboard()
    
    elif callback_data == 'users':
        users = get_user_list()
        if not users:
            return "❌ Пользователи не найдены", get_main_keyboard()
        
        text = "👥 <b>Список пользователей</b>\n\n"
        for user in users[:10]:  # Показываем первых 10
            text += f"<code>{user['username']}</code> (ID: {user['id']})\n"
            text += f"📧 {user['email']}\n"
            text += f"💰 Баланс: {user['balance']}₽\n"
            text += f"📱 Telegram: {user['telegram']} ({user['telegram_status']})\n"
            text += f"📅 Регистрация: {user['created_at']}\n"
            text += f"🔹 {user['status']}\n\n"
        
        if len(users) > 10:
            text += f"... и еще {len(users) - 10} пользователей"
        
        return text, get_main_keyboard()
    
    elif callback_data == 'balance':
        return "💰 <b>Управление балансами</b>\n\nВыберите действие:", get_balance_keyboard()
    
    elif callback_data == 'view_balances':
        users = get_user_list()
        if not users:
            return "❌ Пользователи не найдены", get_balance_keyboard()
        
        text = "💰 <b>Балансы пользователей</b>\n\n"
        for user in users[:15]:  # Показываем первых 15
            text += f"<code>{user['username']}</code> (ID: {user['id']}): {user['balance']}₽\n"
        
        if len(users) > 15:
            text += f"\n... и еще {len(users) - 15} пользователей"
        
        return text, get_balance_keyboard()
    
    elif callback_data == 'change_balance':
        return "💰 <b>Изменение баланса</b>\n\nВведите сумму (например: 1000 или 1500.50)", get_balance_keyboard()
    
    # Обработка действий с конкретным пользователем
    elif callback_data.startswith('balance_user_'):
        user_id = int(callback_data.split('_')[2])
        user = User.query.get(user_id)
        if user:
            return f"💰 <b>Изменение баланса</b>\n\nПользователь: <code>{user.username}</code>\nТекущий баланс: <b>{user.balance}₽</b>\n\nВведите новую сумму:", get_balance_keyboard()
        else:
            return "❌ Пользователь не найден", get_main_keyboard()
    
    elif callback_data.startswith('ban_user_'):
        user_id = int(callback_data.split('_')[2])
        result = ban_user(user_id)
        return result, get_main_keyboard()
    
    elif callback_data.startswith('unban_user_'):
        user_id = int(callback_data.split('_')[2])
        result = unban_user(user_id)
        return result, get_main_keyboard()
    
    elif callback_data.startswith('admin_user_'):
        user_id = int(callback_data.split('_')[2])
        result = make_admin(user_id)
        return result, get_main_keyboard()
    
    elif callback_data.startswith('remove_admin_user_'):
        user_id = int(callback_data.split('_')[3])
        result = remove_admin(user_id)
        return result, get_main_keyboard()
    
    elif callback_data.startswith('delete_user_'):
        user_id = int(callback_data.split('_')[2])
        result = delete_user_admin(user_id)
        return result, get_main_keyboard()
    
    elif callback_data == 'help':
        return """❓ <b>Справка по админ панели</b>

🔧 <b>Основные функции:</b>
• 📊 Статистика - просмотр статистики системы
• 👥 Пользователи - список всех пользователей
• 💰 Баланс - управление балансами пользователей
• 🔧 Управление - управление пользователями

💡 <b>Советы:</b>
• Используйте кнопки для навигации
• Имена пользователей можно копировать по нажатию
• Просто вводите имена и цифры без команд
• Все изменения сохраняются автоматически""", get_main_keyboard()
    
    else:
        return "❌ Неизвестное действие", get_main_keyboard()

def get_updates(offset=None):
    """Получает обновления от Telegram"""
    try:
        url = f"{BASE_URL}{TELEGRAM_BOT_TOKEN}/getUpdates"
        params = {'timeout': 30}
        if offset:
            params['offset'] = offset
        
        response = requests.get(url, params=params, timeout=35)
        return response.json()
    except Exception as e:
        print(f"Get updates error: {e}")
        return None

def telegram_bot_worker():
    """Рабочий поток для Telegram бота"""
    print("🤖 Telegram админский бот запущен!")
    print("📱 Админ chat_id:", ADMIN_CHAT_ID)
    last_update_id = None
    
    while True:
        try:
            updates = get_updates(last_update_id)
            
            if not updates or not updates.get('ok'):
                print("❌ Ошибка получения обновлений")
                time.sleep(5)
                continue
            
            # Обрабатываем каждое обновление
            for update in updates.get('result', []):
                last_update_id = update['update_id'] + 1
                
                # Обрабатываем сообщения
                if 'message' in update:
                    message = update['message']
                    chat_id = str(message['chat']['id'])
                    text = message.get('text', '')
                    
                    print(f"📱 Получено сообщение от {chat_id}: {text}")
                    
                    # Обрабатываем только админ команды
                    if chat_id == ADMIN_CHAT_ID:
                        # Проверяем, ожидается ли изменение баланса
                        if chat_id in pending_balance_change:
                            amount = pending_balance_change[chat_id]
                            result = handle_balance_change(text, amount)
                            del pending_balance_change[chat_id]
                            send_telegram_message(result, chat_id, get_main_keyboard())
                            print(f"✅ Изменен баланс: {result}")
                        else:
                            response, keyboard = handle_admin_command(text, chat_id)
                            send_telegram_message(response, chat_id, keyboard)
                            print(f"✅ Отправлен ответ: {response[:50]}...")
                    else:
                        print(f"⚠️ Сообщение от неадмина: {chat_id}")
                
                # Обрабатываем callback запросы (нажатия на кнопки)
                elif 'callback_query' in update:
                    callback_query = update['callback_query']
                    chat_id = str(callback_query['message']['chat']['id'])
                    callback_data = callback_query['data']
                    
                    print(f"🔘 Получен callback от {chat_id}: {callback_data}")
                    
                    # Обрабатываем только админ callback'и
                    if chat_id == ADMIN_CHAT_ID:
                        response, keyboard = handle_callback_query(callback_data, chat_id)
                        send_telegram_message(response, chat_id, keyboard)
                        print(f"✅ Отправлен ответ на callback: {response[:50]}...")
                        
                        # Отвечаем на callback query
                        try:
                            answer_url = f"{BASE_URL}{TELEGRAM_BOT_TOKEN}/answerCallbackQuery"
                            answer_payload = {'callback_query_id': callback_query['id']}
                            requests.post(answer_url, data=answer_payload, timeout=5)
                        except Exception as e:
                            print(f"❌ Ошибка ответа на callback: {e}")
                    else:
                        print(f"⚠️ Callback от неадмина: {chat_id}")
            
            # Небольшая пауза между запросами
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("👋 Бот остановлен.")
            break
        except Exception as e:
            print(f"❌ Произошла ошибка в основном цикле: {e}")
            time.sleep(5)

def start_telegram_bot():
    """Запускает Telegram бот в отдельном потоке"""
    bot_thread = threading.Thread(target=telegram_bot_worker, daemon=True)
    bot_thread.start()
    print("✅ Telegram бот запущен в фоновом режиме")

if __name__ == '__main__':
    # Запускаем Telegram бот в фоне
    start_telegram_bot()
    
    # Запускаем Flask приложение
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Запуск Flask приложения на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
