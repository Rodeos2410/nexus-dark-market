#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Быстрый тест чата
"""

import os
import sys

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🚀 Быстрый тест чата")
    print("=" * 30)
    
    try:
        # Импортируем необходимые модули
        from app import app, db, User, Product, Message
        print("✅ Импорты успешны")
        
        # Проверяем подключение к базе данных
        with app.app_context():
            # Проверяем таблицы
            user_count = User.query.count()
            product_count = Product.query.count()
            message_count = Message.query.count()
            
            print(f"👥 Пользователей: {user_count}")
            print(f"📦 Товаров: {product_count}")
            print(f"💬 Сообщений: {message_count}")
            
            # Проверяем, есть ли пользователи с товарами
            users_with_products = User.query.join(Product).distinct().count()
            print(f"👤 Пользователей с товарами: {users_with_products}")
            
            if user_count > 0 and product_count > 0:
                print("✅ Есть данные для тестирования чата")
                
                # Показываем пример товара
                product = Product.query.first()
                if product:
                    print(f"📦 Пример товара: {product.name} (продавец: {product.seller.username})")
                    print(f"🔗 URL чата: /chat/{product.id}")
                
                return True
            else:
                print("⚠️ Недостаточно данных для тестирования")
                return False
                
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Чат готов к тестированию!")
        print("\n📋 Для тестирования:")
        print("1. Запустите приложение: python app.py")
        print("2. Зайдите на сайт и авторизуйтесь")
        print("3. Перейдите к любому товару")
        print("4. Нажмите '💬 Написать продавцу'")
        print("5. Отправьте сообщение")
    else:
        print("\n⚠️ Есть проблемы с чатом")
    
    sys.exit(0 if success else 1)
