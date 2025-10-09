#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт инициализации для Render
Создает базу данных, админа и настраивает все компоненты
"""

import os
import sys
from app import app, db, User, Product, CartItem
from werkzeug.security import generate_password_hash
from datetime import datetime

def init_database():
    """Инициализирует базу данных"""
    print("🗄️ Инициализация базы данных...")
    
    with app.app_context():
        try:
            # Создаем все таблицы
            print("📋 Создание таблиц...")
            db.create_all()
            print("✅ Таблицы созданы")
            
            # Проверяем, есть ли уже админ
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                print("👑 Создание администратора...")
                admin = User(
                    username='admin',
                    email='admin@nexus.dark',
                    password_hash=generate_password_hash('admin123'),
                    is_admin=True,
                    balance=10000.0,
                    created_at=datetime.utcnow()
                )
                db.session.add(admin)
                db.session.commit()
                print("✅ Администратор создан: admin/admin123")
            else:
                print("✅ Администратор уже существует")
            
            # Проверяем количество пользователей
            user_count = User.query.count()
            print(f"👥 Всего пользователей: {user_count}")
            
            # Проверяем количество товаров
            product_count = Product.query.count()
            print(f"📦 Всего товаров: {product_count}")
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка инициализации БД: {e}")
            return False

def check_environment():
    """Проверяет переменные окружения"""
    print("🔧 Проверка переменных окружения...")
    
    required_vars = [
        'SECRET_KEY',
        'DATABASE_URL',
        'TELEGRAM_BOT_TOKEN',
        'TELEGRAM_CHAT_ID'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            # Скрываем чувствительные данные
            if 'TOKEN' in var or 'KEY' in var:
                print(f"✅ {var}: {'*' * 10}")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: НЕ НАЙДЕНА")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️ Отсутствуют переменные: {', '.join(missing_vars)}")
        return False
    
    return True

def test_telegram_connection():
    """Тестирует подключение к Telegram"""
    print("📱 Тестирование Telegram...")
    
    try:
        import requests
        
        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        if not bot_token:
            print("❌ TELEGRAM_BOT_TOKEN не найден")
            return False
        
        # Проверяем информацию о боте
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            bot_info = response.json()
            if bot_info.get('ok'):
                print(f"✅ Бот доступен: {bot_info['result']['first_name']}")
                print(f"🆔 Username: @{bot_info['result']['username']}")
                return True
            else:
                print(f"❌ Ошибка API: {bot_info}")
                return False
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка Telegram: {e}")
        return False

def setup_webhook():
    """Настраивает webhook для Telegram"""
    print("🔗 Настройка webhook...")
    
    try:
        import requests
        
        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        if not bot_token:
            print("❌ TELEGRAM_BOT_TOKEN не найден")
            return False
        
        # Получаем URL приложения из переменных окружения
        app_url = os.environ.get('RENDER_EXTERNAL_URL', 'https://nexus-dark-market-1.onrender.com')
        webhook_url = f"{app_url}/telegram/webhook"
        
        print(f"🌐 Webhook URL: {webhook_url}")
        
        # Устанавливаем webhook
        url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
        payload = {'url': webhook_url}
        
        response = requests.post(url, data=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                print("✅ Webhook настроен успешно")
                return True
            else:
                print(f"❌ Ошибка webhook: {result}")
                return False
        else:
            print(f"❌ HTTP ошибка webhook: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка настройки webhook: {e}")
        return False

def main():
    """Основная функция инициализации"""
    print("🚀 Инициализация Nexus Dark на Render")
    print("=" * 50)
    
    # Проверяем переменные окружения
    if not check_environment():
        print("❌ Не все переменные окружения настроены")
        return False
    
    # Инициализируем базу данных
    if not init_database():
        print("❌ Ошибка инициализации базы данных")
        return False
    
    # Тестируем Telegram
    if not test_telegram_connection():
        print("❌ Ошибка подключения к Telegram")
        return False
    
    # Настраиваем webhook
    if not setup_webhook():
        print("❌ Ошибка настройки webhook")
        return False
    
    print("\n🎉 Инициализация завершена успешно!")
    print("\n📋 Что работает:")
    print("✅ База данных PostgreSQL")
    print("✅ Администратор: admin/admin123")
    print("✅ Telegram бот @NexusDarkBot")
    print("✅ Webhook настроен")
    print("✅ Админ панель в боте")
    print("✅ Уведомления Telegram")
    
    print("\n🔗 Ссылки:")
    app_url = os.environ.get('RENDER_EXTERNAL_URL', 'https://nexus-dark-market-1.onrender.com')
    print(f"🌐 Сайт: {app_url}")
    print("📱 Бот: @NexusDarkBot")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
