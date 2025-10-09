#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import psycopg2
from psycopg2.extras import RealDictCursor

def connect_to_render_db():
    """Подключается к PostgreSQL базе данных на Render"""
    
    # Получите эти данные из Render Dashboard
    # Database -> Info -> External Database URL
    DATABASE_URL = "postgresql://username:password@hostname:port/database"
    
    print("🔗 Подключение к базе данных Render...")
    print("=" * 50)
    
    try:
        # Подключаемся к базе данных
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        print("✅ Подключение успешно!")
        
        # Получаем информацию о таблицах
        print("\n📋 Таблицы в базе данных:")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        for table in tables:
            print(f"  📄 {table['table_name']}")
        
        # Показываем пользователей
        print("\n👥 Пользователи:")
        cursor.execute("""
            SELECT id, username, email, balance, telegram_username, 
                   telegram_chat_id, is_admin, is_banned, created_at
            FROM "user" 
            ORDER BY id;
        """)
        
        users = cursor.fetchall()
        print(f"Всего пользователей: {len(users)}")
        print("-" * 80)
        
        for user in users:
            status = "Admin" if user['is_admin'] else ("Banned" if user['is_banned'] else "User")
            telegram_status = "✅ Настроен" if user['telegram_chat_id'] else "❌ Не настроен"
            
            print(f"ID: {user['id']:3d} | {user['username']:15s} | {user['email']:25s} | "
                  f"{user['balance']:8.2f}₽ | {telegram_status:15s} | {status}")
        
        # Показываем товары
        print("\n🛍️ Товары:")
        cursor.execute("""
            SELECT p.id, p.name, p.price, p.stock, u.username as seller
            FROM product p
            JOIN "user" u ON p.seller_id = u.id
            ORDER BY p.id;
        """)
        
        products = cursor.fetchall()
        print(f"Всего товаров: {len(products)}")
        print("-" * 80)
        
        for product in products:
            stock_info = f"Склад: {product['stock']}" if product['stock'] is not None else "Без ограничений"
            print(f"ID: {product['id']:3d} | {product['name']:30s} | "
                  f"{product['price']:8.2f}₽ | {stock_info:15s} | Продавец: {product['seller']}")
        
        cursor.close()
        conn.close()
        
        print("\n✅ Просмотр завершен!")
        
    except psycopg2.Error as e:
        print(f"❌ Ошибка базы данных: {e}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def main():
    """Основная функция"""
    print("🗄️ Просмотр базы данных Render")
    print("=" * 50)
    print("💡 Для использования этого скрипта:")
    print("1. Зайдите в Render Dashboard")
    print("2. Найдите вашу PostgreSQL базу данных")
    print("3. Скопируйте 'External Database URL'")
    print("4. Вставьте URL в переменную DATABASE_URL в этом скрипте")
    print("5. Установите psycopg2: pip install psycopg2-binary")
    print("6. Запустите скрипт")
    print()
    
    # Проверяем, установлен ли psycopg2
    try:
        import psycopg2
        print("✅ psycopg2 установлен")
        connect_to_render_db()
    except ImportError:
        print("❌ psycopg2 не установлен")
        print("💡 Установите: pip install psycopg2-binary")

if __name__ == "__main__":
    main()
