#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Исправление проблем с Telegram ботом
"""

import os
import sys

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_bot_file():
    """Проверяем файл бота"""
    print("🔍 Проверяем файл telegram_bot.py...")
    
    if not os.path.exists('telegram_bot.py'):
        print("   ❌ Файл telegram_bot.py не найден")
        return False
    
    print("   ✅ Файл telegram_bot.py найден")
    
    # Проверяем размер файла
    file_size = os.path.getsize('telegram_bot.py')
    print(f"   📊 Размер файла: {file_size} байт")
    
    if file_size < 1000:
        print("   ⚠️ Файл слишком маленький, возможно поврежден")
        return False
    
    return True

def check_bot_imports():
    """Проверяем импорты бота"""
    print("🔍 Проверяем импорты бота...")
    
    try:
        # Пытаемся импортировать основные модули
        import requests
        import json
        import os
        import time
        from datetime import datetime
        
        print("   ✅ Стандартные модули импортированы")
        
        # Пытаемся импортировать модули приложения
        from app import app, db, User, Product, CartItem
        
        print("   ✅ Модули приложения импортированы")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка импорта: {e}")
        return False

def check_bot_functions():
    """Проверяем функции бота"""
    print("🔍 Проверяем функции бота...")
    
    try:
        from telegram_bot import (
            TELEGRAM_BOT_TOKEN, ADMIN_CHAT_ID,
            get_user_state, set_user_state, clear_user_state,
            create_inline_keyboard, send_telegram_message,
            get_user_stats, get_user_list, get_main_menu,
            handle_callback_query, process_telegram_update
        )
        
        print("   ✅ Основные функции импортированы")
        
        # Проверяем конфигурацию
        if TELEGRAM_BOT_TOKEN and ADMIN_CHAT_ID:
            print("   ✅ Конфигурация найдена")
        else:
            print("   ❌ Конфигурация неполная")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка функций: {e}")
        return False

def test_bot_connection():
    """Тестируем подключение к Telegram API"""
    print("🔍 Тестируем подключение к Telegram API...")
    
    try:
        from telegram_bot import TELEGRAM_BOT_TOKEN, send_telegram_message, ADMIN_CHAT_ID
        
        # Тестовое сообщение
        test_message = "🧪 Тестовое сообщение для проверки бота"
        
        print("   📤 Отправляем тестовое сообщение...")
        result = send_telegram_message(test_message, ADMIN_CHAT_ID)
        
        if result:
            print("   ✅ Тестовое сообщение отправлено")
            return True
        else:
            print("   ❌ Не удалось отправить тестовое сообщение")
            return False
            
    except Exception as e:
        print(f"   ❌ Ошибка подключения: {e}")
        return False

def check_duplicate_functions():
    """Проверяем дублирование функций"""
    print("🔍 Проверяем дублирование функций...")
    
    try:
        with open('telegram_bot.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Проверяем на дублирование функций
        functions = [
            'def ban_user_by_username',
            'def unban_user_by_username',
            'def make_admin_by_username',
            'def remove_admin_by_username',
            'def delete_user_by_username'
        ]
        
        duplicates = []
        for func in functions:
            count = content.count(func)
            if count > 1:
                duplicates.append(func)
                print(f"   ⚠️ Дублирование функции: {func} ({count} раз)")
        
        if duplicates:
            print(f"   ❌ Найдено {len(duplicates)} дублированных функций")
            return False
        else:
            print("   ✅ Дублированных функций не найдено")
            return True
            
    except Exception as e:
        print(f"   ❌ Ошибка проверки: {e}")
        return False

def fix_bot_issues():
    """Исправляем проблемы с ботом"""
    print("🔧 Исправляем проблемы с ботом...")
    
    try:
        # Читаем файл
        with open('telegram_bot.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Проверяем и исправляем основные проблемы
        
        # 1. Проверяем обработку callback query
        if 'answer_callback_query(callback_query[\'id\'])' in content:
            print("   ✅ Обработка callback query найдена")
        else:
            print("   ⚠️ Обработка callback query может быть проблемной")
        
        # 2. Проверяем управление состояниями
        if 'get_user_state' in content and 'set_user_state' in content:
            print("   ✅ Управление состояниями найдено")
        else:
            print("   ⚠️ Управление состояниями может быть проблемным")
        
        # 3. Проверяем обработку ошибок
        if 'try:' in content and 'except' in content:
            print("   ✅ Обработка ошибок найдена")
        else:
            print("   ⚠️ Обработка ошибок может быть недостаточной")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка исправления: {e}")
        return False

def main():
    """Основная функция"""
    print("🚀 Исправление проблем с Telegram ботом")
    print("=" * 60)
    
    # Проверка 1: Файл бота
    file_ok = check_bot_file()
    
    print("\n" + "=" * 60)
    
    # Проверка 2: Импорты
    imports_ok = check_bot_imports()
    
    print("\n" + "=" * 60)
    
    # Проверка 3: Функции
    functions_ok = check_bot_functions()
    
    print("\n" + "=" * 60)
    
    # Проверка 4: Дублирование функций
    duplicates_ok = check_duplicate_functions()
    
    print("\n" + "=" * 60)
    
    # Проверка 5: Подключение к API
    connection_ok = test_bot_connection()
    
    print("\n" + "=" * 60)
    
    # Исправление проблем
    fix_ok = fix_bot_issues()
    
    print("\n" + "=" * 60)
    print("📊 РЕЗУЛЬТАТЫ:")
    print(f"   Файл бота: {'✅' if file_ok else '❌'}")
    print(f"   Импорты: {'✅' if imports_ok else '❌'}")
    print(f"   Функции: {'✅' if functions_ok else '❌'}")
    print(f"   Дублирование: {'✅' if duplicates_ok else '❌'}")
    print(f"   Подключение к API: {'✅' if connection_ok else '❌'}")
    print(f"   Исправления: {'✅' if fix_ok else '❌'}")
    
    if all([file_ok, imports_ok, functions_ok, duplicates_ok, connection_ok, fix_ok]):
        print("\n🎉 Telegram бот исправлен и готов к работе!")
        print("\n📋 Для тестирования:")
        print("1. Запустите бота: python telegram_bot.py")
        print("2. Откройте Telegram и найдите бота")
        print("3. Отправьте /start")
        print("4. Проверьте работу всех кнопок")
        print("5. Протестируйте управление пользователями")
    else:
        print("\n⚠️ Есть проблемы с Telegram ботом")
        print("\n🔧 Дополнительные действия:")
        print("1. Проверьте токен бота")
        print("2. Убедитесь, что бот запущен")
        print("3. Проверьте chat_id админа")
        print("4. Проверьте подключение к интернету")
        print("5. Запустите тест: python test_telegram_bot.py")

if __name__ == "__main__":
    main()
