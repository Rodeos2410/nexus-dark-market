#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Полное исправление системы чата
"""

import os
import sys

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def fix_database():
    """Исправляем базу данных"""
    print("🔧 Исправляем базу данных...")
    
    try:
        from app import app, db, User, Product, Message
        from sqlalchemy import text
        
        with app.app_context():
            # Пересоздаем таблицу message
            try:
                db.session.execute(text("DROP TABLE IF EXISTS message"))
                db.session.commit()
                print("   🗑️ Старая таблица message удалена")
            except Exception as e:
                print(f"   ⚠️ Ошибка удаления таблицы: {e}")
            
            # Создаем новую таблицу
            try:
                db.create_all()
                print("   ✅ Новая таблица message создана")
                
                # Проверяем создание
                message_count = Message.query.count()
                print(f"   📊 Количество сообщений: {message_count}")
                
                return True
                
            except Exception as e:
                print(f"   ❌ Ошибка создания таблицы: {e}")
                return False
                
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return False

def test_message_creation():
    """Тестируем создание сообщения"""
    print("🧪 Тестируем создание сообщения...")
    
    try:
        from app import app, db, User, Product, Message
        
        with app.app_context():
            # Находим пользователя и товар
            user = User.query.first()
            product = Product.query.first()
            
            if not user or not product:
                print("   ❌ Недостаточно данных для тестирования")
                return False
            
            print(f"   👤 Пользователь: {user.username} (ID: {user.id})")
            print(f"   📦 Товар: {product.name} (ID: {product.id})")
            print(f"   👤 Продавец: {product.seller.username} (ID: {product.seller_id})")
            
            # Создаем тестовое сообщение
            test_message = Message(
                sender_id=user.id,
                receiver_id=product.seller_id,
                product_id=product.id,
                content="Тестовое сообщение для проверки чата",
                is_read=False
            )
            
            db.session.add(test_message)
            db.session.commit()
            
            print(f"   ✅ Сообщение создано с ID: {test_message.id}")
            
            # Проверяем сохранение
            saved_message = Message.query.get(test_message.id)
            if saved_message:
                print(f"   ✅ Сообщение найдено: {saved_message.content}")
                
                # Проверяем запрос для чата
                chat_messages = Message.query.filter(
                    ((Message.sender_id == user.id) & (Message.receiver_id == product.seller_id)) |
                    ((Message.sender_id == product.seller_id) & (Message.receiver_id == user.id))
                ).filter(Message.product_id == product.id).order_by(Message.created_at.asc()).all()
                
                print(f"   📝 Сообщений в чате: {len(chat_messages)}")
                
                # Удаляем тестовое сообщение
                db.session.delete(saved_message)
                db.session.commit()
                print("   ✅ Тестовое сообщение удалено")
                
                return True
            else:
                print("   ❌ Сообщение не найдено после сохранения")
                return False
                
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        db.session.rollback()
        return False

def check_telegram_bot():
    """Проверяем Telegram бота"""
    print("🤖 Проверяем Telegram бота...")
    
    try:
        from app import send_telegram_message
        
        # Проверяем, что функция существует
        if callable(send_telegram_message):
            print("   ✅ Функция send_telegram_message найдена")
            
            # Проверяем пользователей с telegram_chat_id
            from app import User
            with app.app_context():
                users_with_telegram = User.query.filter(User.telegram_chat_id.isnot(None)).count()
                print(f"   📱 Пользователей с Telegram: {users_with_telegram}")
                
                if users_with_telegram > 0:
                    # Показываем примеры
                    users = User.query.filter(User.telegram_chat_id.isnot(None)).limit(3).all()
                    for user in users:
                        print(f"      - {user.username}: {user.telegram_chat_id}")
                
                return True
        else:
            print("   ❌ Функция send_telegram_message не найдена")
            return False
            
    except Exception as e:
        print(f"   ❌ Ошибка проверки Telegram: {e}")
        return False

def fix_chat_template():
    """Исправляем шаблон чата"""
    print("🔧 Проверяем шаблон чата...")
    
    try:
        # Проверяем, что файл существует
        if os.path.exists('templates/chat.html'):
            print("   ✅ Файл templates/chat.html существует")
            
            # Читаем файл и проверяем ключевые элементы
            with open('templates/chat.html', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Проверяем наличие ключевых элементов
            checks = [
                ('chat-container', 'Контейнер чата'),
                ('message-form', 'Форма отправки'),
                ('message-input', 'Поле ввода'),
                ('addMessageToChat', 'Функция добавления сообщения'),
                ('fetch(\'/send_message\'', 'AJAX запрос'),
                ('showNotification', 'Функция уведомлений')
            ]
            
            for check, description in checks:
                if check in content:
                    print(f"   ✅ {description} найден")
                else:
                    print(f"   ❌ {description} не найден")
                    return False
            
            return True
        else:
            print("   ❌ Файл templates/chat.html не найден")
            return False
            
    except Exception as e:
        print(f"   ❌ Ошибка проверки шаблона: {e}")
        return False

def create_test_data():
    """Создаем тестовые данные"""
    print("📝 Создаем тестовые данные...")
    
    try:
        from app import app, db, User, Product, Message
        from werkzeug.security import generate_password_hash
        
        with app.app_context():
            # Проверяем, есть ли пользователи
            user_count = User.query.count()
            if user_count == 0:
                print("   👤 Создаем тестового пользователя...")
                test_user = User(
                    username='testuser',
                    email='test@example.com',
                    password_hash=generate_password_hash('password123'),
                    balance=1000.0,
                    telegram_username='testuser',
                    telegram_chat_id='123456789'
                )
                db.session.add(test_user)
                db.session.commit()
                print("   ✅ Тестовый пользователь создан")
            
            # Проверяем, есть ли товары
            product_count = Product.query.count()
            if product_count == 0:
                print("   📦 Создаем тестовый товар...")
                user = User.query.first()
                test_product = Product(
                    name='Тестовый товар',
                    description='Описание тестового товара',
                    price=100.0,
                    stock=10,
                    seller_id=user.id
                )
                db.session.add(test_product)
                db.session.commit()
                print("   ✅ Тестовый товар создан")
            
            print(f"   📊 Пользователей: {User.query.count()}")
            print(f"   📊 Товаров: {Product.query.count()}")
            
            return True
            
    except Exception as e:
        print(f"   ❌ Ошибка создания тестовых данных: {e}")
        return False

def main():
    """Основная функция"""
    print("🚀 Полное исправление системы чата")
    print("=" * 60)
    
    # Шаг 1: Исправляем базу данных
    print("1️⃣ Исправляем базу данных...")
    db_ok = fix_database()
    
    print("\n" + "=" * 60)
    
    # Шаг 2: Создаем тестовые данные
    print("2️⃣ Создаем тестовые данные...")
    data_ok = create_test_data()
    
    print("\n" + "=" * 60)
    
    # Шаг 3: Тестируем создание сообщений
    print("3️⃣ Тестируем создание сообщений...")
    message_ok = test_message_creation()
    
    print("\n" + "=" * 60)
    
    # Шаг 4: Проверяем Telegram бота
    print("4️⃣ Проверяем Telegram бота...")
    telegram_ok = check_telegram_bot()
    
    print("\n" + "=" * 60)
    
    # Шаг 5: Проверяем шаблон чата
    print("5️⃣ Проверяем шаблон чата...")
    template_ok = fix_chat_template()
    
    print("\n" + "=" * 60)
    print("📊 РЕЗУЛЬТАТЫ ИСПРАВЛЕНИЯ:")
    print(f"   База данных: {'✅' if db_ok else '❌'}")
    print(f"   Тестовые данные: {'✅' if data_ok else '❌'}")
    print(f"   Создание сообщений: {'✅' if message_ok else '❌'}")
    print(f"   Telegram бот: {'✅' if telegram_ok else '❌'}")
    print(f"   Шаблон чата: {'✅' if template_ok else '❌'}")
    
    if all([db_ok, data_ok, message_ok, telegram_ok, template_ok]):
        print("\n🎉 Система чата полностью исправлена!")
        print("\n📋 Для тестирования:")
        print("1. Запустите приложение: python app.py")
        print("2. Откройте браузер: http://localhost:5000")
        print("3. Авторизуйтесь (testuser / password123)")
        print("4. Перейдите к товару")
        print("5. Нажмите '💬 Написать продавцу'")
        print("6. Отправьте сообщение")
        print("7. Проверьте консоль браузера (F12)")
        print("8. Проверьте логи приложения")
        return True
    else:
        print("\n⚠️ Есть проблемы с системой чата")
        print("\n🔧 Дополнительные действия:")
        print("1. Проверьте конфигурацию Telegram в config.py")
        print("2. Убедитесь, что бот запущен")
        print("3. Проверьте права доступа к файлам")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
