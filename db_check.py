#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os
import sys

def main():
    print("🔍 Проверка базы данных")
    print("=" * 50)
    
    # Путь к базе данных
    db_path = "instance/nexus_dark.db"
    
    if not os.path.exists(db_path):
        print(f"❌ База данных не найдена: {db_path}")
        return
    
    print(f"✅ База данных найдена: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Проверяем структуру таблицы user
        print("\n📋 Структура таблицы user:")
        cursor.execute("PRAGMA table_info(user)")
        columns = cursor.fetchall()
        
        for col in columns:
            print(f"  - {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'}")
        
        # Проверяем наличие нужных колонок
        column_names = [col[1] for col in columns]
        required_columns = ['telegram_username', 'telegram_chat_id', 'telegram_setup_token']
        
        print("\n🔍 Проверка необходимых колонок:")
        missing_columns = []
        for col in required_columns:
            if col in column_names:
                print(f"  ✅ {col}")
            else:
                print(f"  ❌ {col} - ОТСУТСТВУЕТ!")
                missing_columns.append(col)
        
        # Проверяем данные пользователей
        print("\n👥 Данные пользователей:")
        cursor.execute("SELECT id, username, email, telegram_username, telegram_chat_id, telegram_setup_token FROM user")
        users = cursor.fetchall()
        
        if not users:
            print("  ❌ Пользователи не найдены")
        else:
            for user in users:
                print(f"\n  👤 ID: {user[0]}, Username: {user[1]}")
                print(f"     Email: {user[2]}")
                print(f"     Telegram username: {user[3] or 'Не указан'}")
                print(f"     Telegram chat_id: {user[4] or 'Не настроен'}")
                print(f"     Setup token: {user[5] or 'Не сгенерирован'}")
        
        # Проверяем уникальность токенов
        print("\n🔑 Проверка токенов:")
        cursor.execute("SELECT telegram_setup_token, COUNT(*) FROM user WHERE telegram_setup_token IS NOT NULL GROUP BY telegram_setup_token HAVING COUNT(*) > 1")
        duplicates = cursor.fetchall()
        
        if duplicates:
            print("  ❌ Найдены дублирующиеся токены:")
            for token, count in duplicates:
                print(f"     {token}: {count} раз")
        else:
            print("  ✅ Дублирующихся токенов не найдено")
        
        conn.close()
        
        # Рекомендации
        print("\n" + "=" * 50)
        print("🎯 Рекомендации:")
        
        if missing_columns:
            print("❌ Отсутствуют колонки в базе данных!")
            print("💡 Запустите приложение для автоматической миграции")
            print("💡 Или выполните миграцию вручную")
        else:
            print("✅ Структура базы данных корректна")
        
        print("\n💡 Для тестирования:")
        print("1. Запустите приложение: python app.py")
        print("2. Войдите в аккаунт")
        print("3. Перейдите в профиль")
        print("4. Нажмите 'Настроить уведомления'")
        print("5. Проверьте логи в консоли")
        
    except Exception as e:
        print(f"❌ Ошибка при проверке базы данных: {e}")

if __name__ == "__main__":
    main()



