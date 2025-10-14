#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Исправление доставки сообщений в чат
"""

import os
import sys

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_message_delivery():
    """Проверяем доставку сообщений"""
    print("🔍 Проверяем доставку сообщений в чат")
    print("=" * 50)
    
    try:
        from app import app, db, User, Product, Message
        
        with app.app_context():
            # Проверяем пользователей и товары
            users = User.query.all()
            products = Product.query.all()
            
            if len(users) < 2 or len(products) == 0:
                print("❌ Недостаточно данных для тестирования")
                print(f"   Пользователей: {len(users)}")
                print(f"   Товаров: {len(products)}")
                return False
            
            # Берем первого пользователя и первый товар
            user = users[0]
            product = products[0]
            
            print(f"👤 Тестовый пользователь: {user.username} (ID: {user.id})")
            print(f"📦 Тестовый товар: {product.name} (ID: {product.id})")
            print(f"👤 Продавец товара: {product.seller.username} (ID: {product.seller_id})")
            
            # Проверяем существующие сообщения
            existing_messages = Message.query.filter(
                ((Message.sender_id == user.id) & (Message.receiver_id == product.seller_id)) |
                ((Message.sender_id == product.seller_id) & (Message.receiver_id == user.id))
            ).filter(Message.product_id == product.id).all()
            
            print(f"📝 Существующих сообщений в чате: {len(existing_messages)}")
            
            # Создаем тестовое сообщение
            print("\n📤 Создаем тестовое сообщение...")
            test_message = Message(
                sender_id=user.id,
                receiver_id=product.seller_id,
                product_id=product.id,
                content="Тестовое сообщение для проверки доставки",
                is_read=False
            )
            
            db.session.add(test_message)
            db.session.commit()
            
            print(f"✅ Сообщение создано с ID: {test_message.id}")
            
            # Проверяем, что сообщение появилось в запросе чата
            print("\n🔍 Проверяем запрос чата...")
            chat_messages = Message.query.filter(
                ((Message.sender_id == user.id) & (Message.receiver_id == product.seller_id)) |
                ((Message.sender_id == product.seller_id) & (Message.receiver_id == user.id))
            ).filter(Message.product_id == product.id).order_by(Message.created_at.asc()).all()
            
            print(f"📝 Сообщений в запросе чата: {len(chat_messages)}")
            
            # Проверяем, что наше сообщение есть в списке
            found_message = False
            for msg in chat_messages:
                if msg.id == test_message.id:
                    found_message = True
                    print(f"✅ Тестовое сообщение найдено в запросе чата")
                    break
            
            if not found_message:
                print("❌ Тестовое сообщение не найдено в запросе чата")
                return False
            
            # Проверяем отображение сообщений
            print("\n📋 Список всех сообщений в чате:")
            for i, msg in enumerate(chat_messages, 1):
                sender = User.query.get(msg.sender_id)
                receiver = User.query.get(msg.receiver_id)
                print(f"   {i}. От {sender.username} к {receiver.username}: {msg.content}")
                print(f"      Время: {msg.created_at.strftime('%H:%M')}, Прочитано: {msg.is_read}")
            
            # Удаляем тестовое сообщение
            db.session.delete(test_message)
            db.session.commit()
            print("\n✅ Тестовое сообщение удалено")
            
            return True
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_chat_route_simulation():
    """Симулируем работу маршрута чата"""
    print("\n🔍 Симулируем работу маршрута чата")
    print("=" * 50)
    
    try:
        from app import app, db, User, Product, Message
        
        with app.app_context():
            # Находим товар
            product = Product.query.first()
            if not product:
                print("❌ Товары не найдены")
                return False
            
            # Находим пользователя
            user = User.query.first()
            if not user:
                print("❌ Пользователи не найдены")
                return False
            
            print(f"📦 Товар: {product.name} (ID: {product.id})")
            print(f"👤 Пользователь: {user.username} (ID: {user.id})")
            print(f"👤 Продавец: {product.seller.username} (ID: {product.seller_id})")
            
            # Симулируем логику маршрута chat_with_seller
            print("\n🔄 Симулируем логику маршрута...")
            
            # Получаем сообщения между пользователями
            messages = Message.query.filter(
                ((Message.sender_id == user.id) & (Message.receiver_id == product.seller_id)) |
                ((Message.sender_id == product.seller_id) & (Message.receiver_id == user.id))
            ).filter(Message.product_id == product.id).order_by(Message.created_at.asc()).all()
            
            print(f"📝 Найдено сообщений: {len(messages)}")
            
            # Отмечаем сообщения как прочитанные
            read_count = 0
            for message in messages:
                if message.receiver_id == user.id and not message.is_read:
                    message.is_read = True
                    read_count += 1
            
            if read_count > 0:
                db.session.commit()
                print(f"✅ Отмечено как прочитанных: {read_count}")
            
            # Проверяем данные для шаблона
            print("\n📊 Данные для шаблона:")
            print(f"   product.name: {product.name}")
            print(f"   product.seller.username: {product.seller.username}")
            print(f"   messages|length: {len(messages)}")
            
            if messages:
                print("   📋 Сообщения:")
                for msg in messages:
                    sender = User.query.get(msg.sender_id)
                    print(f"      - {msg.sender.username}: {msg.content[:50]}...")
            
            return True
            
    except Exception as e:
        print(f"❌ Ошибка симуляции: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Основная функция"""
    print("🚀 Исправление доставки сообщений в чат")
    print("=" * 50)
    
    # Тест 1: Проверка доставки сообщений
    delivery_ok = check_message_delivery()
    
    # Тест 2: Симуляция маршрута чата
    route_ok = test_chat_route_simulation()
    
    print("\n" + "=" * 50)
    print("📊 РЕЗУЛЬТАТЫ:")
    print(f"   Доставка сообщений: {'✅' if delivery_ok else '❌'}")
    print(f"   Маршрут чата: {'✅' if route_ok else '❌'}")
    
    if delivery_ok and route_ok:
        print("\n🎉 Система доставки сообщений работает!")
        print("\n📋 Для тестирования в браузере:")
        print("1. Запустите приложение: python app.py")
        print("2. Откройте браузер: http://localhost:5000")
        print("3. Авторизуйтесь")
        print("4. Перейдите к товару")
        print("5. Нажмите '💬 Написать продавцу'")
        print("6. Отправьте сообщение")
        print("7. Проверьте консоль браузера (F12) для отладочной информации")
        print("8. Проверьте логи приложения в терминале")
    else:
        print("\n⚠️ Есть проблемы с доставкой сообщений")
        print("\n🔧 Возможные решения:")
        print("1. Пересоздайте таблицу: python fix_message_table.py")
        print("2. Проверьте базу данных")
        print("3. Перезапустите приложение")
        print("4. Проверьте логи в консоли браузера")

if __name__ == "__main__":
    main()
