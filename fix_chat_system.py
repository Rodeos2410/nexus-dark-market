#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт для проверки и исправления системы чата
"""

import os
import sys
from datetime import datetime

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, Product, Message

def check_database_tables():
    """Проверяем существование таблиц в базе данных"""
    print("🔍 Проверяем таблицы в базе данных...")
    
    with app.app_context():
        try:
            # Получаем список таблиц
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"📋 Найденные таблицы: {tables}")
            
            # Проверяем наличие таблицы message
            if 'message' in tables:
                print("✅ Таблица 'message' существует")
                
                # Проверяем структуру таблицы
                columns = inspector.get_columns('message')
                print(f"📊 Колонки таблицы 'message': {[col['name'] for col in columns]}")
                
                # Проверяем количество сообщений
                message_count = Message.query.count()
                print(f"💬 Количество сообщений в базе: {message_count}")
                
                return True
            else:
                print("❌ Таблица 'message' не найдена")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка при проверке таблиц: {e}")
            return False

def create_message_table():
    """Создаем таблицу message если её нет"""
    print("🔧 Создаем таблицу 'message'...")
    
    with app.app_context():
        try:
            # Создаем все таблицы
            db.create_all()
            print("✅ Таблица 'message' создана")
            return True
        except Exception as e:
            print(f"❌ Ошибка при создании таблицы: {e}")
            return False

def test_message_creation():
    """Тестируем создание сообщения"""
    print("🧪 Тестируем создание сообщения...")
    
    with app.app_context():
        try:
            # Находим первого пользователя
            user = User.query.first()
            if not user:
                print("❌ Пользователи не найдены")
                return False
            
            # Создаем тестовое сообщение
            test_message = Message(
                sender_id=user.id,
                receiver_id=user.id,  # Отправляем самому себе для теста
                content="Тестовое сообщение для проверки чата",
                is_read=False
            )
            
            db.session.add(test_message)
            db.session.commit()
            
            print(f"✅ Тестовое сообщение создано с ID: {test_message.id}")
            
            # Удаляем тестовое сообщение
            db.session.delete(test_message)
            db.session.commit()
            
            print("✅ Тестовое сообщение удалено")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при тестировании сообщения: {e}")
            db.session.rollback()
            return False

def check_chat_routes():
    """Проверяем маршруты чата"""
    print("🔍 Проверяем маршруты чата...")
    
    with app.app_context():
        try:
            # Проверяем, что маршруты зарегистрированы
            routes = [rule.rule for rule in app.url_map.iter_rules()]
            
            chat_routes = [route for route in routes if 'chat' in route or 'message' in route]
            print(f"📋 Маршруты чата: {chat_routes}")
            
            required_routes = ['/chat/<int:product_id>', '/send_message', '/messages']
            missing_routes = []
            
            for required_route in required_routes:
                if not any(required_route.replace('<int:product_id>', '') in route for route in routes):
                    missing_routes.append(required_route)
            
            if missing_routes:
                print(f"❌ Отсутствующие маршруты: {missing_routes}")
                return False
            else:
                print("✅ Все маршруты чата присутствуют")
                return True
                
        except Exception as e:
            print(f"❌ Ошибка при проверке маршрутов: {e}")
            return False

def check_telegram_integration():
    """Проверяем интеграцию с Telegram"""
    print("🔍 Проверяем интеграцию с Telegram...")
    
    with app.app_context():
        try:
            # Проверяем функцию send_telegram_message
            from app import send_telegram_message
            
            # Проверяем, что функция существует
            if callable(send_telegram_message):
                print("✅ Функция send_telegram_message найдена")
                
                # Проверяем пользователей с telegram_chat_id
                users_with_telegram = User.query.filter(User.telegram_chat_id.isnot(None)).count()
                print(f"📱 Пользователей с настроенным Telegram: {users_with_telegram}")
                
                return True
            else:
                print("❌ Функция send_telegram_message не найдена")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка при проверке Telegram интеграции: {e}")
            return False

def main():
    """Основная функция"""
    print("🚀 Запуск проверки системы чата...")
    print("=" * 50)
    
    # Проверяем таблицы
    tables_ok = check_database_tables()
    if not tables_ok:
        print("\n🔧 Создаем недостающие таблицы...")
        create_ok = create_message_table()
        if not create_ok:
            print("❌ Не удалось создать таблицы")
            return False
    
    print("\n" + "=" * 50)
    
    # Тестируем создание сообщений
    message_ok = test_message_creation()
    
    print("\n" + "=" * 50)
    
    # Проверяем маршруты
    routes_ok = check_chat_routes()
    
    print("\n" + "=" * 50)
    
    # Проверяем Telegram интеграцию
    telegram_ok = check_telegram_integration()
    
    print("\n" + "=" * 50)
    print("📊 РЕЗУЛЬТАТЫ ПРОВЕРКИ:")
    print(f"   Таблицы БД: {'✅' if tables_ok else '❌'}")
    print(f"   Создание сообщений: {'✅' if message_ok else '❌'}")
    print(f"   Маршруты чата: {'✅' if routes_ok else '❌'}")
    print(f"   Telegram интеграция: {'✅' if telegram_ok else '❌'}")
    
    if all([tables_ok, message_ok, routes_ok, telegram_ok]):
        print("\n🎉 Система чата работает корректно!")
        return True
    else:
        print("\n⚠️ Обнаружены проблемы в системе чата")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
