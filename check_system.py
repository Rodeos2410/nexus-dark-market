#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import sqlite3
from app import app, db, User, Product, CartItem

def check_database():
    """Проверяет состояние базы данных"""
    print("🔍 Проверка базы данных...")
    
    try:
        with app.app_context():
            # Проверяем подключение к базе
            db.engine.connect()
            print("✅ Подключение к базе данных: OK")
            
            # Проверяем таблицы
            tables = ['user', 'product', 'cart_item']
            for table in tables:
                try:
                    result = db.engine.execute(f"SELECT COUNT(*) FROM {table}")
                    count = result.fetchone()[0]
                    print(f"✅ Таблица {table}: {count} записей")
                except Exception as e:
                    print(f"❌ Таблица {table}: ОШИБКА - {e}")
            
            # Проверяем структуру таблицы product
            try:
                result = db.engine.execute("PRAGMA table_info(product)")
                columns = [row[1] for row in result]
                print(f"📋 Столбцы таблицы product: {columns}")
                
                if 'stock' in columns:
                    print("✅ Столбец 'stock' существует")
                else:
                    print("❌ Столбец 'stock' отсутствует")
            except Exception as e:
                print(f"❌ Ошибка проверки структуры product: {e}")
            
            # Проверяем структуру таблицы user
            try:
                result = db.engine.execute("PRAGMA table_info(user)")
                columns = [row[1] for row in result]
                print(f"📋 Столбцы таблицы user: {columns}")
                
                required_columns = ['telegram_username', 'telegram_chat_id', 'is_banned', 'is_admin']
                for col in required_columns:
                    if col in columns:
                        print(f"✅ Столбец '{col}' существует")
                    else:
                        print(f"❌ Столбец '{col}' отсутствует")
            except Exception as e:
                print(f"❌ Ошибка проверки структуры user: {e}")
                
    except Exception as e:
        print(f"❌ Ошибка подключения к базе данных: {e}")

def check_files():
    """Проверяет наличие необходимых файлов"""
    print("\n🔍 Проверка файлов...")
    
    required_files = [
        'app.py',
        'admin_bot.py',
        'config.py',
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        '.gitignore',
        'README.md'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - отсутствует")
    
    # Проверяем папки
    required_dirs = ['templates', 'static', 'instance']
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ Папка {dir_name}/")
        else:
            print(f"❌ Папка {dir_name}/ - отсутствует")

def check_telegram():
    """Проверяет настройки Telegram"""
    print("\n🔍 Проверка Telegram...")
    
    try:
        import requests
        
        # Проверяем токен бота
        token = '8458514538:AAFIAT7BrKelIHie9-JscBnOlAFd_V2qyMY'
        url = f"https://api.telegram.org/bot{token}/getMe"
        
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data['result']
                print(f"✅ Telegram бот: @{bot_info['username']} ({bot_info['first_name']})")
            else:
                print(f"❌ Telegram бот: Ошибка - {data}")
        else:
            print(f"❌ Telegram бот: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка проверки Telegram: {e}")

def main():
    print("🛒 Nexus Dark Market - Проверка системы")
    print("=" * 50)
    
    check_files()
    check_database()
    check_telegram()
    
    print("\n" + "=" * 50)
    print("✅ Проверка завершена!")

if __name__ == "__main__":
    main()
