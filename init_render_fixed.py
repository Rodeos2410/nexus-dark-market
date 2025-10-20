#!/usr/bin/env python3
"""
Скрипт для инициализации Nexus Dark на Render с исправлениями
"""

import os
import sys
import requests
import json
from datetime import datetime

def check_environment():
    """Проверяет переменные окружения"""
    print("🔧 Проверка окружения...")
    print("=" * 50)
    
    # Проверяем обязательные переменные
    required_vars = {
        'SECRET_KEY': os.environ.get('SECRET_KEY'),
        'DATABASE_URL': os.environ.get('DATABASE_URL'),
        'TELEGRAM_BOT_TOKEN': os.environ.get('TELEGRAM_BOT_TOKEN'),
        'TELEGRAM_CHAT_ID': os.environ.get('TELEGRAM_CHAT_ID')
    }
    
    for var_name, var_value in required_vars.items():
        if var_value:
            if 'TOKEN' in var_name or 'KEY' in var_name:
                print(f"✅ {var_name}: {'*' * 10}")
            else:
                print(f"✅ {var_name}: {var_value[:50]}...")
        else:
            print(f"❌ {var_name}: НЕ УСТАНОВЛЕН")
    
    print("=" * 50)
    return all(required_vars.values())

def test_database():
    """Тестирует подключение к базе данных"""
    print("🗄️ Инициализация базы данных...")
    print("=" * 50)
    
    try:
        from app import app, db, User, Product, Message
        from werkzeug.security import generate_password_hash
        
        with app.app_context():
            # Создаем таблицы
            print("📋 Создание таблиц...")
            db.create_all()
            print("✅ Таблицы созданы")
            
            # Проверяем админа
            admin_exists = User.query.filter_by(is_admin=True).first()
            if not admin_exists:
                admin = User(
                    username='Rodeos',
                    email='rodeos@nexus.dark',
                    password_hash=generate_password_hash('Rodeos24102007'),
                    balance=10000.0,
                    is_admin=True,
                    is_banned=False,
                    telegram_chat_id='1172834372'
                )
                db.session.add(admin)
                db.session.commit()
                print("✅ Администратор создан: Rodeos")
            else:
                print(f"✅ Администратор уже существует: {admin_exists.username}")
            
            # Статистика
            total_users = User.query.count()
            total_products = Product.query.count()
            print(f"👥 Всего пользователей: {total_users}")
            print(f"📦 Всего товаров: {total_products}")
            
        return True
        
    except Exception as e:
        print(f"❌ Ошибка базы данных: {e}")
        return False

def test_telegram():
    """Тестирует Telegram API"""
    print("📱 Тестирование Telegram...")
    print("=" * 50)
    
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID', '1172834372')
    
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN не установлен")
        return False
    
    try:
        # Проверяем токен
        url = f"https://api.telegram.org/bot{token}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data.get('result', {})
                print(f"✅ Токен валиден!")
                print(f"🤖 Имя бота: {bot_info.get('first_name', 'N/A')}")
                print(f"🆔 Username: @{bot_info.get('username', 'N/A')}")
                
                # Тестируем отправку
                test_url = f"https://api.telegram.org/bot{token}/sendMessage"
                test_payload = {
                    'chat_id': chat_id,
                    'text': '🧪 Тестовое сообщение от Nexus Dark',
                    'parse_mode': 'HTML'
                }
                
                test_response = requests.post(test_url, data=test_payload, timeout=10)
                if test_response.status_code == 200:
                    test_data = test_response.json()
                    if test_data.get('ok'):
                        print("✅ Тестовое сообщение отправлено успешно")
                        return True
                    else:
                        print(f"❌ Ошибка отправки: {test_data}")
                        return False
                else:
                    print(f"❌ HTTP ошибка: {test_response.status_code}")
                    return False
            else:
                print(f"❌ Ошибка API: {data}")
                return False
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка подключения к Telegram: {e}")
        return False

def main():
    """Основная функция"""
    print("🚀 Инициализация Nexus Dark на Render")
    print("=" * 50)
    
    # Проверяем окружение
    if not check_environment():
        print("❌ Не все переменные окружения установлены!")
        print("🔧 Установите следующие переменные в настройках Render:")
        print("   - SECRET_KEY")
        print("   - DATABASE_URL")
        print("   - TELEGRAM_BOT_TOKEN")
        print("   - TELEGRAM_CHAT_ID")
        return False
    
    # Тестируем базу данных
    if not test_database():
        print("❌ Ошибка инициализации базы данных")
        return False
    
    # Тестируем Telegram
    if not test_telegram():
        print("❌ Ошибка подключения к Telegram")
        return False
    
    print("=" * 50)
    print("✅ Инициализация завершена успешно!")
    print("🌐 Приложение готово к работе")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
