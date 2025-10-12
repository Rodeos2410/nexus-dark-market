#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диагностика проблем с чатом
"""

import os
import sys
import requests
import json
import time

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_database_connection():
    """Тестируем подключение к базе данных"""
    print("🔍 Тестируем подключение к базе данных...")
    
    try:
        from app import app, db, User, Product, Message
        
        with app.app_context():
            # Проверяем таблицы
            user_count = User.query.count()
            product_count = Product.query.count()
            message_count = Message.query.count()
            
            print(f"   👥 Пользователей: {user_count}")
            print(f"   📦 Товаров: {product_count}")
            print(f"   💬 Сообщений: {message_count}")
            
            # Проверяем структуру таблицы message
            try:
                # Получаем информацию о колонках
                inspector = db.inspect(db.engine)
                columns = inspector.get_columns('message')
                print(f"   📊 Колонки таблицы message: {[col['name'] for col in columns]}")
                
                # Проверяем последние сообщения
                recent_messages = Message.query.order_by(Message.created_at.desc()).limit(5).all()
                print(f"   📝 Последние сообщения: {len(recent_messages)}")
                
                for msg in recent_messages:
                    print(f"      - ID: {msg.id}, От: {msg.sender_id}, К: {msg.receiver_id}, Товар: {msg.product_id}")
                
                return True
                
            except Exception as e:
                print(f"   ❌ Ошибка проверки таблицы message: {e}")
                return False
                
    except Exception as e:
        print(f"   ❌ Ошибка подключения к БД: {e}")
        return False

def test_message_creation():
    """Тестируем создание сообщения"""
    print("🔍 Тестируем создание сообщения...")
    
    try:
        from app import app, db, User, Product, Message
        
        with app.app_context():
            # Находим пользователя и товар
            user = User.query.first()
            product = Product.query.first()
            
            if not user:
                print("   ❌ Пользователи не найдены")
                return False
                
            if not product:
                print("   ❌ Товары не найдены")
                return False
            
            print(f"   👤 Тестовый пользователь: {user.username} (ID: {user.id})")
            print(f"   📦 Тестовый товар: {product.name} (ID: {product.id})")
            
            # Создаем тестовое сообщение
            test_message = Message(
                sender_id=user.id,
                receiver_id=product.seller_id,
                product_id=product.id,
                content="Тестовое сообщение для диагностики",
                is_read=False
            )
            
            db.session.add(test_message)
            db.session.commit()
            
            print(f"   ✅ Сообщение создано с ID: {test_message.id}")
            
            # Проверяем, что сообщение сохранилось правильно
            saved_message = Message.query.get(test_message.id)
            if saved_message:
                print(f"   ✅ Сообщение найдено: {saved_message.content}")
                print(f"   📊 Данные: От {saved_message.sender_id} к {saved_message.receiver_id}, товар {saved_message.product_id}")
                
                # Удаляем тестовое сообщение
                db.session.delete(saved_message)
                db.session.commit()
                print("   ✅ Тестовое сообщение удалено")
                
                return True
            else:
                print("   ❌ Сообщение не найдено после сохранения")
                return False
                
    except Exception as e:
        print(f"   ❌ Ошибка создания сообщения: {e}")
        db.session.rollback()
        return False

def test_chat_queries():
    """Тестируем запросы чата"""
    print("🔍 Тестируем запросы чата...")
    
    try:
        from app import app, db, User, Product, Message
        
        with app.app_context():
            # Находим пользователя и товар
            user = User.query.first()
            product = Product.query.first()
            
            if not user or not product:
                print("   ❌ Недостаточно данных для тестирования")
                return False
            
            # Тестируем запрос сообщений между пользователями
            messages = Message.query.filter(
                ((Message.sender_id == user.id) & (Message.receiver_id == product.seller_id)) |
                ((Message.sender_id == product.seller_id) & (Message.receiver_id == user.id))
            ).filter(Message.product_id == product.id).order_by(Message.created_at.asc()).all()
            
            print(f"   📝 Найдено сообщений между пользователями: {len(messages)}")
            
            # Тестируем запрос всех диалогов пользователя
            sent_messages = Message.query.filter(Message.sender_id == user.id).all()
            received_messages = Message.query.filter(Message.receiver_id == user.id).all()
            
            print(f"   📤 Отправленных сообщений: {len(sent_messages)}")
            print(f"   📥 Полученных сообщений: {len(received_messages)}")
            
            # Собираем уникальные диалоги
            dialogues = {}
            for message in sent_messages + received_messages:
                other_user_id = message.receiver_id if message.sender_id == user.id else message.sender_id
                if other_user_id not in dialogues:
                    dialogues[other_user_id] = {
                        'user': User.query.get(other_user_id),
                        'last_message': message,
                        'unread_count': 0
                    }
                else:
                    if message.created_at > dialogues[other_user_id]['last_message'].created_at:
                        dialogues[other_user_id]['last_message'] = message
                
                if message.receiver_id == user.id and not message.is_read:
                    dialogues[other_user_id]['unread_count'] += 1
            
            print(f"   💬 Уникальных диалогов: {len(dialogues)}")
            
            return True
            
    except Exception as e:
        print(f"   ❌ Ошибка запросов чата: {e}")
        return False

def test_web_interface():
    """Тестируем веб-интерфейс"""
    print("🔍 Тестируем веб-интерфейс...")
    
    base_url = "http://localhost:5000"
    
    try:
        # Проверяем доступность главной страницы
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"   🏠 Главная страница: {response.status_code}")
        
        # Проверяем маршрут сообщений
        response = requests.get(f"{base_url}/messages", timeout=5)
        print(f"   💬 Страница сообщений: {response.status_code}")
        
        # Проверяем маршрут отправки сообщений
        response = requests.get(f"{base_url}/send_message", timeout=5)
        print(f"   📤 Отправка сообщений (GET): {response.status_code}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Ошибка подключения к веб-интерфейсу: {e}")
        return False

def check_message_relationships():
    """Проверяем связи между сообщениями"""
    print("🔍 Проверяем связи между сообщениями...")
    
    try:
        from app import app, db, User, Product, Message
        
        with app.app_context():
            # Проверяем сообщения с некорректными связями
            messages_without_sender = Message.query.filter(~Message.sender_id.in_([u.id for u in User.query.all()])).all()
            messages_without_receiver = Message.query.filter(~Message.receiver_id.in_([u.id for u in User.query.all()])).all()
            messages_without_product = Message.query.filter(
                Message.product_id.isnot(None),
                ~Message.product_id.in_([p.id for p in Product.query.all()])
            ).all()
            
            print(f"   ❌ Сообщений с несуществующим отправителем: {len(messages_without_sender)}")
            print(f"   ❌ Сообщений с несуществующим получателем: {len(messages_without_receiver)}")
            print(f"   ❌ Сообщений с несуществующим товаром: {len(messages_without_product)}")
            
            if messages_without_sender or messages_without_receiver or messages_without_product:
                print("   ⚠️ Обнаружены сообщения с некорректными связями!")
                return False
            else:
                print("   ✅ Все связи корректны")
                return True
                
    except Exception as e:
        print(f"   ❌ Ошибка проверки связей: {e}")
        return False

def main():
    """Основная функция диагностики"""
    print("🚀 Диагностика проблем с чатом")
    print("=" * 50)
    
    # Тест 1: Подключение к базе данных
    db_ok = test_database_connection()
    
    print("\n" + "=" * 50)
    
    # Тест 2: Создание сообщений
    message_ok = test_message_creation()
    
    print("\n" + "=" * 50)
    
    # Тест 3: Запросы чата
    queries_ok = test_chat_queries()
    
    print("\n" + "=" * 50)
    
    # Тест 4: Веб-интерфейс
    web_ok = test_web_interface()
    
    print("\n" + "=" * 50)
    
    # Тест 5: Связи между сообщениями
    relationships_ok = check_message_relationships()
    
    print("\n" + "=" * 50)
    print("📊 РЕЗУЛЬТАТЫ ДИАГНОСТИКИ:")
    print(f"   База данных: {'✅' if db_ok else '❌'}")
    print(f"   Создание сообщений: {'✅' if message_ok else '❌'}")
    print(f"   Запросы чата: {'✅' if queries_ok else '❌'}")
    print(f"   Веб-интерфейс: {'✅' if web_ok else '❌'}")
    print(f"   Связи сообщений: {'✅' if relationships_ok else '❌'}")
    
    if all([db_ok, message_ok, queries_ok, relationships_ok]):
        print("\n🎉 Система чата работает корректно!")
        if web_ok:
            print("   ✅ Все компоненты готовы к работе")
        else:
            print("   ⚠️ Запустите приложение для полного тестирования")
        return True
    else:
        print("\n⚠️ Обнаружены проблемы в системе чата")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
