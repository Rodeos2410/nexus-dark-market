#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os

def migrate_database():
    """Принудительно добавляет недостающие колонки в базу данных"""
    
    print("🔄 Миграция базы данных")
    print("=" * 40)
    
    db_path = "instance/nexus_dark.db"
    
    if not os.path.exists(db_path):
        print(f"❌ База данных не найдена: {db_path}")
        return False
    
    print(f"✅ База данных найдена: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Проверяем текущую структуру
        print("\n📋 Текущая структура таблицы user:")
        cursor.execute("PRAGMA table_info(user)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # Список колонок для добавления
        columns_to_add = [
            ('telegram_username', 'VARCHAR(100)'),
            ('telegram_chat_id', 'VARCHAR(50)'),
            ('telegram_setup_token', 'VARCHAR(100)'),
            ('is_banned', 'BOOLEAN DEFAULT 0'),
            ('is_admin', 'BOOLEAN DEFAULT 0')
        ]
        
        # Добавляем недостающие колонки
        print("\n🔄 Добавление недостающих колонок:")
        for col_name, col_type in columns_to_add:
            if col_name not in column_names:
                try:
                    sql = f"ALTER TABLE user ADD COLUMN {col_name} {col_type}"
                    print(f"  🔄 Добавляем {col_name}...")
                    cursor.execute(sql)
                    print(f"  ✅ {col_name} добавлена")
                except Exception as e:
                    print(f"  ❌ Ошибка добавления {col_name}: {e}")
            else:
                print(f"  ✅ {col_name} уже существует")
        
        # Проверяем структуру после миграции
        print("\n📋 Структура таблицы user после миграции:")
        cursor.execute("PRAGMA table_info(user)")
        columns = cursor.fetchall()
        
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # Проверяем данные пользователей
        print("\n👥 Данные пользователей:")
        cursor.execute("SELECT id, username, telegram_setup_token, telegram_chat_id FROM user")
        users = cursor.fetchall()
        
        for user in users:
            print(f"  👤 ID: {user[0]}, Username: {user[1]}")
            print(f"     Token: {user[2] or 'Не сгенерирован'}")
            print(f"     Chat ID: {user[3] or 'Не настроен'}")
        
        conn.commit()
        conn.close()
        
        print("\n✅ Миграция завершена успешно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при миграции: {e}")
        return False

if __name__ == "__main__":
    migrate_database()