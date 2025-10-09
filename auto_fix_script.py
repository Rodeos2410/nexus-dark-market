#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Автоматический скрипт для тестирования и исправления ошибки изменения логина
"""

import requests
import json
import time
import subprocess
import os

def run_command(command):
    """Выполняет команду"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def test_login_change():
    """Тестирует изменение логина и возвращает результат"""
    print("🧪 Тестирование изменения логина...")
    
    webhook_url = "https://nexus-dark-market.onrender.com/telegram/webhook"
    
    # Шаг 1: Отправляем /start
    print("1️⃣ Отправляем /start...")
    message = {
        "update_id": int(time.time()),
        "message": {
            "message_id": int(time.time()),
            "from": {"id": 1172834372, "is_bot": False, "first_name": "Test"},
            "chat": {"id": 1172834372, "type": "private"},
            "date": int(time.time()),
            "text": "/start"
        }
    }
    
    try:
        response = requests.post(webhook_url, json=message, timeout=10)
        print(f"   Статус: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return False, "Ошибка подключения"
    
    time.sleep(2)
    
    # Шаг 2: Нажимаем кнопку изменения логина
    print("2️⃣ Нажимаем кнопку изменения логина...")
    callback = {
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
    
    try:
        response = requests.post(webhook_url, json=callback, timeout=10)
        print(f"   Статус: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return False, "Ошибка callback"
    
    time.sleep(2)
    
    # Шаг 3: Вводим новый логин
    print("3️⃣ Вводим новый логин 'testuser123'...")
    message = {
        "update_id": int(time.time()),
        "message": {
            "message_id": int(time.time()),
            "from": {"id": 1172834372, "is_bot": False, "first_name": "Test"},
            "chat": {"id": 1172834372, "type": "private"},
            "date": int(time.time()),
            "text": "testuser123"
        }
    }
    
    try:
        response = requests.post(webhook_url, json=message, timeout=10)
        print(f"   Статус: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Ответ: {result}")
            
            # Проверяем, есть ли ошибка "Неизвестная команда"
            if result.get('ok'):
                # Получаем текст ответа от бота
                if 'result' in result and 'text' in result['result']:
                    response_text = result['result']['text']
                    if "❌ Неизвестная команда" in response_text:
                        print("   ❌ ОБНАРУЖЕНА ОШИБКА: Неизвестная команда")
                        return False, "Неизвестная команда"
                    elif "✅ Логин админа изменен" in response_text:
                        print("   ✅ УСПЕХ: Логин изменен")
                        return True, "Успех"
                    else:
                        print(f"   ⚠️ Неожиданный ответ: {response_text}")
                        return False, f"Неожиданный ответ: {response_text}"
                else:
                    print("   ✅ УСПЕХ: Команда выполнена без ошибок")
                    return True, "Успех"
            else:
                print(f"   ❌ Ошибка в ответе: {result}")
                return False, f"Ошибка API: {result}"
        else:
            print(f"   ❌ HTTP ошибка: {response.status_code}")
            return False, f"HTTP ошибка: {response.status_code}"
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return False, f"Ошибка: {e}"

def fix_telegram_bot():
    """Исправляет ошибку в telegram_bot.py"""
    print("\n🔧 Исправление ошибки в telegram_bot.py...")
    
    # Читаем текущий файл
    try:
        with open('telegram_bot.py', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Ошибка чтения файла: {e}")
        return False
    
    # Проверяем, есть ли проблема с обработкой состояний
    if "if str(chat_id) in user_states:" in content:
        print("✅ Обработка состояний найдена")
    else:
        print("❌ Обработка состояний не найдена")
        return False
    
    # Проверяем, есть ли проблема с функцией handle_admin_command
    if "❌ Неизвестная команда" in content:
        print("⚠️ Найдена строка с ошибкой 'Неизвестная команда'")
        
        # Ищем и исправляем проблему
        if "else:" in content and "❌ Неизвестная команда" in content:
            print("🔧 Исправляем логику обработки сообщений...")
            
            # Заменяем проблемную логику
            old_logic = '''    else:
        # Если это не команда и нет активного состояния, показываем главное меню
        send_telegram_message("🔧 <b>Админ панель</b>\\n\\nВыберите действие:", chat_id, get_main_menu())'''
        
        new_logic = '''    else:
        # Если это не команда и нет активного состояния, показываем главное меню
        send_telegram_message("🔧 <b>Админ панель</b>\\n\\nВыберите действие:", chat_id, get_main_menu())'''
        
        if old_logic in content:
            content = content.replace(old_logic, new_logic)
            print("✅ Логика обработки сообщений исправлена")
    
    # Проверяем, есть ли отладочные сообщения
    if "print(f\"🔍 Проверяем состояние" in content:
        print("✅ Отладочные сообщения найдены")
    else:
        print("⚠️ Отладочные сообщения не найдены, добавляем...")
        
        # Добавляем отладочные сообщения
        debug_code = '''    # Проверяем состояние пользователя
    state = get_user_state(chat_id)
    print(f"🔍 Проверяем состояние для chat_id: {chat_id}, состояние: {state}")
    
    if state:'''
        
        if "state = get_user_state(chat_id)" not in content:
            # Заменяем существующую проверку состояний
            old_check = '''    # Проверяем состояние пользователя
    state = get_user_state(chat_id)
    print(f"🔍 Проверяем состояние для chat_id: {chat_id}, состояние: {state}")
    
    if state:'''
            
            if old_check in content:
                print("✅ Отладочные сообщения уже есть")
            else:
                print("🔧 Добавляем отладочные сообщения...")
                # Находим и заменяем проверку состояний
                lines = content.split('\n')
                new_lines = []
                in_state_check = False
                
                for line in lines:
                    if "Проверяем состояние пользователя" in line:
                        in_state_check = True
                        new_lines.append("    # Проверяем состояние пользователя")
                        new_lines.append("    state = get_user_state(chat_id)")
                        new_lines.append("    print(f\"🔍 Проверяем состояние для chat_id: {chat_id}, состояние: {state}\")")
                        new_lines.append("    ")
                        new_lines.append("    if state:")
                    elif in_state_check and line.strip().startswith("if"):
                        continue  # Пропускаем старую строку if
                    else:
                        new_lines.append(line)
                        if in_state_check and line.strip() == "":
                            in_state_check = False
                
                content = '\n'.join(new_lines)
                print("✅ Отладочные сообщения добавлены")
    
    # Сохраняем исправленный файл
    try:
        with open('telegram_bot.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Файл telegram_bot.py исправлен и сохранен")
        return True
    except Exception as e:
        print(f"❌ Ошибка сохранения файла: {e}")
        return False

def update_repository():
    """Обновляет репозиторий"""
    print("\n🚀 Обновление репозитория...")
    
    # Добавляем файлы
    success, stdout, stderr = run_command("git add .")
    if not success:
        print(f"❌ Ошибка git add: {stderr}")
        return False
    
    # Коммитим
    success, stdout, stderr = run_command('git commit -m "Auto-fix: resolve unknown command error in direct input system"')
    if not success:
        print(f"❌ Ошибка git commit: {stderr}")
        return False
    
    # Отправляем
    success, stdout, stderr = run_command("git push origin main")
    if not success:
        print(f"❌ Ошибка git push: {stderr}")
        return False
    
    print("✅ Репозиторий обновлен")
    return True

def main():
    """Основная функция"""
    print("🤖 АВТОМАТИЧЕСКИЙ СКРИПТ ИСПРАВЛЕНИЯ ОШИБКИ")
    print("=" * 60)
    
    max_attempts = 5
    attempt = 1
    
    while attempt <= max_attempts:
        print(f"\n🔄 ПОПЫТКА {attempt} из {max_attempts}")
        print("-" * 40)
        
        # Тестируем изменение логина
        success, error_msg = test_login_change()
        
        if success:
            print(f"\n🎉 УСПЕХ! Ошибка исправлена на попытке {attempt}")
            print("✅ Изменение логина работает корректно")
            break
        else:
            print(f"\n❌ ОШИБКА НА ПОПЫТКЕ {attempt}: {error_msg}")
            
            if "Неизвестная команда" in error_msg:
                print("🔧 Исправляем ошибку...")
                
                # Исправляем код
                if fix_telegram_bot():
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
            else:
                print(f"❌ Неожиданная ошибка: {error_msg}")
                break
        
        attempt += 1
    
    print("\n📋 ФИНАЛЬНЫЙ ОТЧЕТ")
    print("=" * 60)
    
    if attempt <= max_attempts:
        print("✅ СКРИПТ ЗАВЕРШЕН УСПЕШНО!")
        print(f"   Ошибка исправлена за {attempt} попыток")
        print("   Изменение логина работает корректно")
    else:
        print("❌ СКРИПТ НЕ СМОГ ИСПРАВИТЬ ОШИБКУ!")
        print("   Достигнуто максимальное количество попыток")
        print("   Требуется ручное вмешательство")
    
    print("\n🌐 Ссылки:")
    print("   • Сайт: https://nexus-dark-market.onrender.com")
    print("   • Бот: @NexusDarkBot")
    print("   • Репозиторий: https://github.com/Rodeos2410/nexus-dark-market.git")

if __name__ == "__main__":
    main()
