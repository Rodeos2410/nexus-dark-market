import sqlite3
import os

print("🔍 Проверка базы данных")
print("=" * 40)

db_path = "instance/nexus_dark.db"

if not os.path.exists(db_path):
    print(f"❌ База данных не найдена: {db_path}")
    exit()

print(f"✅ База данных найдена: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Проверяем структуру таблицы user
    print("\n📋 Структура таблицы user:")
    cursor.execute("PRAGMA table_info(user)")
    columns = cursor.fetchall()
    
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    
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
    cursor.execute("SELECT id, username, telegram_username, telegram_chat_id, telegram_setup_token FROM user")
    users = cursor.fetchall()
    
    if not users:
        print("  ❌ Пользователи не найдены")
    else:
        for user in users:
            print(f"\n  👤 ID: {user[0]}, Username: {user[1]}")
            print(f"     Telegram username: {user[2] or 'Не указан'}")
            print(f"     Telegram chat_id: {user[3] or 'Не настроен'}")
            print(f"     Setup token: {user[4] or 'Не сгенерирован'}")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Ошибка при проверке базы данных: {e}")


