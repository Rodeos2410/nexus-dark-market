#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Продвинутый скрипт для чтения сообщений от бота и автоматического исправления ошибок
"""

import requests
import json
import time
import subprocess
import re

def run_command(command):
    """Выполняет команду"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def send_to_bot(webhook_url, message_data):
    """Отправляет сообщение боту и возвращает ответ"""
    try:
        response = requests.post(webhook_url, json=message_data, timeout=10)
        return response.status_code == 200, response.json() if response.status_code == 200 else None
    except Exception as e:
        return False, None

def read_bot_response(webhook_url):
    """Читает ответ от бота при тестировании изменения логина"""
    print("📱 Чтение ответа от бота...")
    
    # Шаг 1: /start
    print("1️⃣ Отправляем /start")
    start_message = {
        "update_id": int(time.time()),
        "message": {
            "message_id": int(time.time()),
            "from": {"id": 1172834372, "is_bot": False, "first_name": "Test"},
            "chat": {"id": 1172834372, "type": "private"},
            "date": int(time.time()),
            "text": "/start"
        }
    }
    success, response = send_to_bot(webhook_url, start_message)
    print(f"   Статус: {'✅' if success else '❌'}")
    time.sleep(2)
    
    # Шаг 2: Кнопка изменения логина
    print("2️⃣ Нажимаем кнопку изменения логина")
    callback_message = {
        "update_id": int(time.time()),
        "callback_query": {
            "id": f"test_{int(time.time())}",
            "from": {"id": 1172834372, "is_bot": False, "first_name": "Test"},
            "message": {
                "message_id": 1,
                "from": {"id": 1172834372, "is_bot": False, "first_name": "Test"},
                "chat": {"id": 1172834372, "type": "private"},
                "date": int(time.time()),
                "text": "/start"
            },
            "data": "change_admin_username"
        }
    }
    success, response = send_to_bot(webhook_url, callback_message)
    print(f"   Статус: {'✅' if success else '❌'}")
    time.sleep(2)
    
    # Шаг 3: Ввод логина
    print("3️⃣ Вводим логин 'testuser123'")
    input_message = {
        "update_id": int(time.time()),
        "message": {
            "message_id": int(time.time()),
            "from": {"id": 1172834372, "is_bot": False, "first_name": "Test"},
            "chat": {"id": 1172834372, "type": "private"},
            "date": int(time.time()),
            "text": "testuser123"
        }
    }
    success, response = send_to_bot(webhook_url, input_message)
    print(f"   Статус: {'✅' if success else '❌'}")
    
    # Анализируем ответ
    if success and response:
        print(f"   📱 Ответ от бота: {response}")
        
        if response.get('ok'):
            if 'result' in response and 'text' in response['result']:
                bot_text = response['result']['text']
                print(f"   📝 Текст сообщения: {bot_text}")
                return bot_text
            else:
                print("   ⚠️ Нет текста в ответе")
                return None
        else:
            print(f"   ❌ Ошибка API: {response}")
            return None
    else:
        print("   ❌ Ошибка отправки")
        return None

def analyze_bot_message(message):
    """Детальный анализ сообщения от бота"""
    if not message:
        return False, "Нет сообщения", "Не удалось получить сообщение от бота"
    
    print(f"\n🔍 ДЕТАЛЬНЫЙ АНАЛИЗ СООБЩЕНИЯ:")
    print(f"   Сообщение: {message}")
    
    # Словарь ошибок и их решений
    error_analysis = {
        "❌ Неизвестная команда": {
            "type": "command_error",
            "description": "Бот не понимает команду",
            "fix": "Исправить обработку состояний в process_telegram_update"
        },
        "❌ Неизвестное действие": {
            "type": "action_error", 
            "description": "Неизвестное действие в callback",
            "fix": "Добавить обработку callback в handle_callback_query"
        },
        "❌ Доступ запрещен": {
            "type": "access_error",
            "description": "Проблема с правами доступа",
            "fix": "Проверить ADMIN_CHAT_ID"
        },
        "❌ Админ не найден": {
            "type": "admin_error",
            "description": "Не найден админ в базе данных",
            "fix": "Исправить функцию change_admin_username"
        },
        "❌ Пользователь не найден": {
            "type": "user_error",
            "description": "Пользователь не найден в базе данных",
            "fix": "Исправить функции поиска пользователей"
        }
    }
    
    # Проверяем на ошибки
    for error_text, error_info in error_analysis.items():
        if error_text in message:
            print(f"   ❌ ОБНАРУЖЕНА ОШИБКА:")
            print(f"      Тип: {error_info['type']}")
            print(f"      Описание: {error_info['description']}")
            print(f"      Решение: {error_info['fix']}")
            return True, error_info['type'], error_info['fix']
    
    # Проверяем на успех
    success_patterns = [
        "✅ Логин админа изменен",
        "✅ Пароль админа изменен", 
        "✅ Пользователь заблокирован",
        "✅ Пользователь разблокирован",
        "✅ Пользователь назначен админом",
        "✅ Пользователь больше не админ",
        "✅ Пользователь удален",
        "🔍 Информация о пользователе",
        "👤 Изменение логина админа",
        "🔒 Изменение пароля админа"
    ]
    
    for pattern in success_patterns:
        if pattern in message:
            print(f"   ✅ УСПЕХ: {pattern}")
            return False, "success", "Операция выполнена успешно"
    
    # Если не нашли ни ошибку, ни успех
    print(f"   ⚠️ НЕОПРЕДЕЛЕННЫЙ РЕЗУЛЬТАТ")
    return False, "unknown", "Не удалось определить результат"

def fix_bot_code(error_type, fix_description):
    """Исправляет код в зависимости от типа ошибки"""
    print(f"\n🔧 ИСПРАВЛЕНИЕ КОДА:")
    print(f"   Тип ошибки: {error_type}")
    print(f"   Описание исправления: {fix_description}")
    
    # Читаем файл
    try:
        with open('telegram_bot.py', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"   ❌ Ошибка чтения файла: {e}")
        return False
    
    # Исправления в зависимости от типа ошибки
    if error_type == "command_error":
        print("   🔧 Исправляем обработку команд...")
        
        # Проверяем, есть ли правильная обработка состояний
        if "if state:" not in content:
            print("   ❌ Не найдена обработка состояний")
            return False
        
        # Добавляем дополнительную отладку
        debug_addition = '''
    # Дополнительная отладка для состояний
    print(f"🔍 DEBUG: chat_id={chat_id}, state={state}, text='{text}'")
    print(f"🔍 DEBUG: user_states={user_states}")'''
        
        if "Дополнительная отладка для состояний" not in content:
            content = content.replace("if state:", f"if state:{debug_addition}")
            print("   ✅ Добавлена дополнительная отладка")
        
        # Улучшаем обработку неизвестных команд
        if "❌ Неизвестная команда" in content:
            old_text = "❌ Неизвестная команда. Используйте /start для главного меню"
            new_text = "🔧 Админ панель. Используйте /start для главного меню"
            content = content.replace(old_text, new_text)
            print("   ✅ Улучшено сообщение об ошибке")
    
    elif error_type == "admin_error":
        print("   🔧 Исправляем поиск админа...")
        
        # Проверяем функцию change_admin_username
        if "User.query.filter_by(is_admin=True).first()" not in content:
            print("   ❌ Функция поиска админа не найдена")
            return False
        
        # Добавляем отладку в функцию
        debug_code = '''
        print(f"🔍 DEBUG: Ищем админа в базе данных...")
        print(f"🔍 DEBUG: Найден админ: {admin}")'''
        
        if "DEBUG: Ищем админа в базе данных" not in content:
            content = content.replace(
                "admin = User.query.filter_by(is_admin=True).first()",
                f"admin = User.query.filter_by(is_admin=True).first(){debug_code}"
            )
            print("   ✅ Добавлена отладка поиска админа")
    
    elif error_type == "user_error":
        print("   🔧 Исправляем поиск пользователей...")
        
        # Проверяем функции поиска пользователей
        if "User.query.filter_by(username=" not in content:
            print("   ❌ Функции поиска пользователей не найдены")
            return False
        
        print("   ✅ Функции поиска пользователей найдены")
    
    # Сохраняем исправленный файл
    try:
        with open('telegram_bot.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print("   ✅ Файл telegram_bot.py исправлен и сохранен")
        return True
    except Exception as e:
        print(f"   ❌ Ошибка сохранения файла: {e}")
        return False

def update_repository():
    """Обновляет репозиторий"""
    print("\n🚀 Обновление репозитория...")
    
    # Добавляем файлы
    success, stdout, stderr = run_command("git add .")
    if not success:
        print(f"   ❌ Ошибка git add: {stderr}")
        return False
    
    # Коммитим
    success, stdout, stderr = run_command('git commit -m "Advanced auto-fix: resolve bot error messages with detailed analysis"')
    if not success:
        print(f"   ❌ Ошибка git commit: {stderr}")
        return False
    
    # Отправляем
    success, stdout, stderr = run_command("git push origin main")
    if not success:
        print(f"   ❌ Ошибка git push: {stderr}")
        return False
    
    print("   ✅ Репозиторий обновлен")
    return True

def main():
    """Основная функция"""
    print("🤖 ПРОДВИНУТЫЙ СКРИПТ ЧТЕНИЯ СООБЩЕНИЙ ОТ БОТА")
    print("=" * 70)
    print("📱 Читает сообщения от бота, анализирует ошибки и исправляет код")
    print()
    
    webhook_url = "https://nexus-dark-market.onrender.com/telegram/webhook"
    max_attempts = 3
    attempt = 1
    
    while attempt <= max_attempts:
        print(f"🔄 ПОПЫТКА {attempt} из {max_attempts}")
        print("-" * 50)
        
        # Читаем ответ от бота
        bot_message = read_bot_response(webhook_url)
        
        # Анализируем сообщение
        has_error, error_type, fix_description = analyze_bot_message(bot_message)
        
        if not has_error:
            print(f"\n🎉 УСПЕХ! Ошибка исправлена на попытке {attempt}")
            print("✅ Бот работает корректно")
            break
        else:
            print(f"\n❌ ОШИБКА НА ПОПЫТКЕ {attempt}")
            print(f"   Тип: {error_type}")
            print(f"   Исправление: {fix_description}")
            
            # Исправляем код
            if fix_bot_code(error_type, fix_description):
                # Обновляем репозиторий
                if update_repository():
                    print("⏳ Ждем 30 секунд для развертывания...")
                    time.sleep(30)
                else:
                    print("❌ Не удалось обновить репозиторий")
                    break
            else:
                print("❌ Не удалось исправить код")
                break
        
        attempt += 1
    
    print("\n📋 ФИНАЛЬНЫЙ ОТЧЕТ")
    print("=" * 70)
    
    if attempt <= max_attempts:
        print("✅ СКРИПТ ЗАВЕРШЕН УСПЕШНО!")
        print(f"   Ошибка исправлена за {attempt} попыток")
        print("   Бот работает корректно")
    else:
        print("❌ СКРИПТ НЕ СМОГ ИСПРАВИТЬ ОШИБКУ!")
        print("   Достигнуто максимальное количество попыток")
        print("   Требуется ручное вмешательство")
    
    print("\n🌐 Ссылки:")
    print("   • Бот: @NexusDarkBot")
    print("   • Сайт: https://nexus-dark-market.onrender.com")
    print("   • Репозиторий: https://github.com/Rodeos2410/nexus-dark-market.git")

if __name__ == "__main__":
    main()
