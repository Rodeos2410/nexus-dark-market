#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Исправление таблицы сообщений
"""

import os
import sys

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def recreate_message_table():
    """Пересоздаем таблицу сообщений"""
    print("🔧 Пересоздаем таблицу сообщений...")
    
    try:
        from app import app, db, Message
        from sqlalchemy import text
        
        with app.app_context():
            # Проверяем, существует ли таблица
            try:
                message_count = Message.query.count()
                print(f"   📊 Текущее количество сообщений: {message_count}")
            except Exception as e:
                print(f"   ⚠️ Проблема с таблицей: {e}")
            
            # Удаляем таблицу если существует
            try:
                db.session.execute(text("DROP TABLE IF EXISTS message"))
                db.session.commit()
                print("   🗑️ Старая таблица удалена")
            except Exception as e:
                print(f"   ⚠️ Ошибка удаления таблицы: {e}")
            
            # Создаем новую таблицу
            try:
                db.create_all()
                print("   ✅ Новая таблица создана")
                
                # Проверяем создание
                message_count = Message.query.count()
                print(f"   📊 Количество сообщений в новой таблице: {message_count}")
                
                return True
                
            except Exception as e:
                print(f"   ❌ Ошибка создания таблицы: {e}")
                return False
                
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return False

def test_message_operations():
    """Тестируем операции с сообщениями"""
    print("🧪 Тестируем операции с сообщениями...")
    
    try:
        from app import app, db, User, Product, Message
        
        with app.app_context():
            # Находим пользователя и товар
            user = User.query.first()
            product = Product.query.first()
            
            if not user or not product:
                print("   ❌ Недостаточно данных для тестирования")
                return False
            
            print(f"   👤 Тестовый пользователь: {user.username}")
            print(f"   📦 Тестовый товар: {product.name}")
            
            # Создаем тестовое сообщение
            test_message = Message(
                sender_id=user.id,
                receiver_id=product.seller_id,
                product_id=product.id,
                content="Тестовое сообщение для проверки",
                is_read=False
            )
            
            db.session.add(test_message)
            db.session.commit()
            
            print(f"   ✅ Сообщение создано с ID: {test_message.id}")
            
            # Проверяем сохранение
            saved_message = Message.query.get(test_message.id)
            if saved_message:
                print(f"   ✅ Сообщение найдено: {saved_message.content}")
                
                # Проверяем связи
                sender = User.query.get(saved_message.sender_id)
                receiver = User.query.get(saved_message.receiver_id)
                product_obj = Product.query.get(saved_message.product_id)
                
                print(f"   👤 Отправитель: {sender.username if sender else 'Не найден'}")
                print(f"   👤 Получатель: {receiver.username if receiver else 'Не найден'}")
                print(f"   📦 Товар: {product_obj.name if product_obj else 'Не найден'}")
                
                # Удаляем тестовое сообщение
                db.session.delete(saved_message)
                db.session.commit()
                print("   ✅ Тестовое сообщение удалено")
                
                return True
            else:
                print("   ❌ Сообщение не найдено после сохранения")
                return False
                
    except Exception as e:
        print(f"   ❌ Ошибка тестирования: {e}")
        db.session.rollback()
        return False

def check_message_relationships():
    """Проверяем связи сообщений"""
    print("🔍 Проверяем связи сообщений...")
    
    try:
        from app import app, db, User, Product, Message
        
        with app.app_context():
            # Получаем все сообщения
            messages = Message.query.all()
            print(f"   📝 Всего сообщений: {len(messages)}")
            
            if len(messages) == 0:
                print("   ℹ️ Сообщений нет")
                return True
            
            # Проверяем каждое сообщение
            problems = 0
            for message in messages:
                sender = User.query.get(message.sender_id)
                receiver = User.query.get(message.receiver_id)
                product = Product.query.get(message.product_id) if message.product_id else None
                
                if not sender:
                    print(f"   ❌ Сообщение {message.id}: отправитель {message.sender_id} не найден")
                    problems += 1
                
                if not receiver:
                    print(f"   ❌ Сообщение {message.id}: получатель {message.receiver_id} не найден")
                    problems += 1
                
                if message.product_id and not product:
                    print(f"   ❌ Сообщение {message.id}: товар {message.product_id} не найден")
                    problems += 1
            
            if problems == 0:
                print("   ✅ Все связи корректны")
                return True
            else:
                print(f"   ⚠️ Найдено проблем: {problems}")
                return False
                
    except Exception as e:
        print(f"   ❌ Ошибка проверки связей: {e}")
        return False

def main():
    """Основная функция"""
    print("🚀 Исправление таблицы сообщений")
    print("=" * 50)
    
    # Шаг 1: Проверяем текущее состояние
    print("1️⃣ Проверяем текущее состояние...")
    check_message_relationships()
    
    print("\n" + "=" * 50)
    
    # Шаг 2: Пересоздаем таблицу
    print("2️⃣ Пересоздаем таблицу...")
    recreate_ok = recreate_message_table()
    
    print("\n" + "=" * 50)
    
    # Шаг 3: Тестируем операции
    print("3️⃣ Тестируем операции...")
    test_ok = test_message_operations()
    
    print("\n" + "=" * 50)
    
    # Шаг 4: Финальная проверка
    print("4️⃣ Финальная проверка...")
    final_ok = check_message_relationships()
    
    print("\n" + "=" * 50)
    print("📊 РЕЗУЛЬТАТЫ:")
    print(f"   Пересоздание таблицы: {'✅' if recreate_ok else '❌'}")
    print(f"   Тестирование операций: {'✅' if test_ok else '❌'}")
    print(f"   Финальная проверка: {'✅' if final_ok else '❌'}")
    
    if all([recreate_ok, test_ok, final_ok]):
        print("\n🎉 Таблица сообщений исправлена!")
        print("\n📋 Теперь можно тестировать чат:")
        print("1. Запустите приложение: python app.py")
        print("2. Откройте браузер и авторизуйтесь")
        print("3. Перейдите к товару и нажмите '💬 Написать продавцу'")
        print("4. Отправьте сообщение")
        return True
    else:
        print("\n⚠️ Есть проблемы с таблицей сообщений")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
