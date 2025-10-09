#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт для проверки базы данных и отладки системы токенов
"""

import sqlite3
import os
from datetime import datetime

def check_database():
    """Проверяет структуру базы данных и данные пользователей"""
    
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
        for col in required_columns:
            if col in column_names:
                print(f"  ✅ {col}")
            else:
                print(f"  ❌ {col} - ОТСУТСТВУЕТ!")
        
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
        
    except Exception as e:
        print(f"❌ Ошибка при проверке базы данных: {e}")

def test_token_generation():
    """Тестирует генерацию токенов"""
    
    print("\n🧪 Тестирование генерации токенов")
    print("=" * 50)
    
    import secrets
    import string
    
    def generate_telegram_setup_token():
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(32))
    
    # Генерируем несколько токенов для теста
    tokens = []
    for i in range(5):
        token = generate_telegram_setup_token()
        tokens.append(token)
        print(f"  {i+1}. {token}")
    
    # Проверяем уникальность
    if len(set(tokens)) == len(tokens):
        print("  ✅ Все токены уникальны")
    else:
        print("  ❌ Найдены дублирующиеся токены")
    
    # Проверяем длину
    for i, token in enumerate(tokens):
        if len(token) == 32:
            print(f"  ✅ Токен {i+1}: правильная длина")
        else:
            print(f"  ❌ Токен {i+1}: неправильная длина ({len(token)})")

def check_webhook_url():
    """Проверяет настройки webhook"""
    
    print("\n🔗 Проверка webhook")
    print("=" * 50)
    
    # Проверяем, есть ли файл с настройками бота
    bot_token = "8458514538:AAFIAT7BrKelIHie9-JscBnOlAFd_V2qyMY"
    webhook_url = "https://your-domain.com/telegram/webhook"  # Замените на ваш домен
    
    print(f"Bot Token: {bot_token[:10]}...")
    print(f"Webhook URL: {webhook_url}")
    print("\n💡 Для настройки webhook выполните:")
    print(f"curl -X POST \"https://api.telegram.org/bot{bot_token}/setWebhook\" -d \"url={webhook_url}\"")

if __name__ == "__main__":
    check_database()
    test_token_generation()
    check_webhook_url()
    
    print("\n" + "=" * 50)
    print("🎯 Рекомендации:")
    print("1. Убедитесь, что все необходимые колонки существуют в БД")
    print("2. Проверьте, что webhook настроен правильно")
    print("3. Запустите приложение и проверьте логи")
    print("4. Протестируйте генерацию токенов через веб-интерфейс")


