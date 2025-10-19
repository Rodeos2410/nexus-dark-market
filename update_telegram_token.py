#!/usr/bin/env python3
"""
Скрипт для обновления токена Telegram бота
"""

import os
import re

def update_token_in_file(file_path, new_token):
    """Обновляет токен в файле"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Заменяем токен в файле
        old_pattern = r"TELEGRAM_BOT_TOKEN.*?=.*?['\"]([^'\"]+)['\"]"
        new_line = f"TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '{new_token}')"
        
        if 'os.getenv' in content:
            new_line = f"TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '{new_token}')"
        
        updated_content = re.sub(old_pattern, new_line, content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ Токен обновлен в {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при обновлении {file_path}: {e}")
        return False

def main():
    """Основная функция"""
    print("🔧 Обновление токена Telegram бота...")
    
    # Запрашиваем новый токен
    new_token = input("Введите новый токен бота: ").strip()
    
    if not new_token:
        print("❌ Токен не может быть пустым!")
        return False
    
    # Проверяем формат токена
    if not re.match(r'^\d+:[A-Za-z0-9_-]+$', new_token):
        print("❌ Неверный формат токена!")
        print("💡 Токен должен быть в формате: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz")
        return False
    
    # Обновляем токен в файлах
    files_to_update = ['app.py', 'telegram_bot.py']
    success_count = 0
    
    for file_path in files_to_update:
        if os.path.exists(file_path):
            if update_token_in_file(file_path, new_token):
                success_count += 1
        else:
            print(f"⚠️ Файл {file_path} не найден")
    
    if success_count > 0:
        print(f"\n🎉 Токен обновлен в {success_count} файлах!")
        print("\n📝 Следующие шаги:")
        print("1. Обновите переменную TELEGRAM_BOT_TOKEN на Render")
        print("2. Перезапустите приложение")
        print("3. Протестируйте бота")
        return True
    else:
        print("\n❌ Не удалось обновить токен ни в одном файле!")
        return False

if __name__ == "__main__":
    main()
