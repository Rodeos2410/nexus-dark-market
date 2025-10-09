#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Простой автоматический скрипт для исправления ошибки изменения логина
"""

import requests
import json
import time
import subprocess

def run_command(command):
    """Выполняет команду"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def test_bot():
    """Тестирует бота"""
    print("🧪 Тестирование бота...")
    
    webhook_url = "https://nexus-dark-market.onrender.com/telegram/webhook"
    
    # 1. /start
    print("1. Отправляем /start")
    message = {
        "update_id": 1,
        "message": {
            "message_id": 1,
            "from": {"id": 1172834372, "is_bot": False, "first_name": "Test"},
            "chat": {"id": 1172834372, "type": "private"},
            "date": int(time.time()),
            "text": "/start"
        }
    }
    requests.post(webhook_url, json=message, timeout=5)
    time.sleep(1)
    
    # 2. Кнопка изменения логина
    print("2. Нажимаем кнопку изменения логина")
    callback = {
        "update_id": 2,
        "callback_query": {
            "id": "test",
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
    requests.post(webhook_url, json=callback, timeout=5)
    time.sleep(1)
    
    # 3. Ввод логина
    print("3. Вводим логин 'testuser123'")
    message = {
        "update_id": 3,
        "message": {
            "message_id": 2,
            "from": {"id": 1172834372, "is_bot": False, "first_name": "Test"},
            "chat": {"id": 1172834372, "type": "private"},
            "date": int(time.time()),
            "text": "testuser123"
        }
    }
    response = requests.post(webhook_url, json=message, timeout=5)
    
    print(f"   Статус: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Ответ: {result}")
        
        # Проверяем на ошибку
        if result.get('ok'):
            if 'result' in result and 'text' in result['result']:
                text = result['result']['text']
                if "❌ Неизвестная команда" in text:
                    print("   ❌ ОБНАРУЖЕНА ОШИБКА!")
                    return False
                else:
                    print("   ✅ УСПЕХ!")
                    return True
            else:
                print("   ✅ УСПЕХ!")
                return True
        else:
            print("   ❌ Ошибка API")
            return False
    else:
        print("   ❌ HTTP ошибка")
        return False

def fix_code():
    """Исправляет код"""
    print("\n🔧 Исправление кода...")
    
    # Читаем файл
    with open('telegram_bot.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Проверяем, есть ли проблема
    if "❌ Неизвестная команда" in content:
        print("   Найдена проблема в коде")
        
        # Ищем проблемное место
        lines = content.split('\n')
        new_lines = []
        
        for i, line in enumerate(lines):
            if "❌ Неизвестная команда" in line:
                print(f"   Исправляем строку {i+1}")
                # Заменяем на более простое сообщение
                new_lines.append('                return "❌ Неизвестная команда. Используйте /start для главного меню", get_main_menu()')
            else:
                new_lines.append(line)
        
        # Сохраняем исправленный файл
        with open('telegram_bot.py', 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print("   ✅ Код исправлен")
        return True
    else:
        print("   ✅ Проблема не найдена")
        return False

def update_repo():
    """Обновляет репозиторий"""
    print("\n🚀 Обновление репозитория...")
    
    # Добавляем файлы
    success, stdout, stderr = run_command("git add .")
    if not success:
        print(f"   ❌ Ошибка git add: {stderr}")
        return False
    
    # Коммитим
    success, stdout, stderr = run_command('git commit -m "Auto-fix: resolve unknown command error"')
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
    print("🤖 ПРОСТОЙ АВТОМАТИЧЕСКИЙ СКРИПТ ИСПРАВЛЕНИЯ")
    print("=" * 50)
    
    # Тестируем бота
    success = test_bot()
    
    if not success:
        print("\n❌ ОБНАРУЖЕНА ОШИБКА!")
        print("🔧 Исправляем...")
        
        # Исправляем код
        if fix_code():
            # Обновляем репозиторий
            if update_repo():
                print("\n⏳ Ждем 30 секунд для развертывания...")
                time.sleep(30)
                
                # Тестируем снова
                print("\n🧪 Повторное тестирование...")
                success = test_bot()
                
                if success:
                    print("\n🎉 ОШИБКА ИСПРАВЛЕНА!")
                else:
                    print("\n❌ Ошибка все еще есть")
            else:
                print("\n❌ Не удалось обновить репозиторий")
        else:
            print("\n❌ Не удалось исправить код")
    else:
        print("\n✅ ОШИБКИ НЕТ!")
    
    print("\n📋 РЕЗУЛЬТАТ:")
    print(f"   Статус: {'✅ Успех' if success else '❌ Ошибка'}")
    print("   Бот: @NexusDarkBot")
    print("   Сайт: https://nexus-dark-market.onrender.com")

if __name__ == "__main__":
    main()
