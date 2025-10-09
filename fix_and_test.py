#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Автоматическое исправление и тестирование изменения логина
"""

import subprocess
import requests
import json
import time

def run_command(command):
    """Выполняет команду"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def update_repository():
    """Обновляет репозиторий"""
    print("🚀 Обновление репозитория...")
    
    # Добавляем файлы
    success, stdout, stderr = run_command("git add .")
    if not success:
        print(f"❌ Ошибка git add: {stderr}")
        return False
    
    # Коммитим
    success, stdout, stderr = run_command('git commit -m "Fix chat_id type consistency and add debug logging"')
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

def test_login_change():
    """Тестирует изменение логина"""
    print("\n🧪 Тестирование изменения логина...")
    
    webhook_url = "https://nexus-dark-market.onrender.com/telegram/webhook"
    
    # Шаг 1: /start
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
        return False
    
    time.sleep(2)
    
    # Шаг 2: Кнопка изменения логина
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
        return False
    
    time.sleep(2)
    
    # Шаг 3: Ввод нового логина
    print("3️⃣ Вводим новый логин...")
    message = {
        "update_id": int(time.time()),
        "message": {
            "message_id": int(time.time()),
            "from": {"id": 1172834372, "is_bot": False, "first_name": "Test"},
            "chat": {"id": 1172834372, "type": "private"},
            "date": int(time.time()),
            "text": "testadmin123"
        }
    }
    
    try:
        response = requests.post(webhook_url, json=message, timeout=10)
        print(f"   Статус: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Ответ: {result}")
            if result.get('ok'):
                print("   ✅ Логин изменен успешно!")
                return True
            else:
                print(f"   ❌ Ошибка в ответе: {result}")
                return False
        else:
            print(f"   ❌ HTTP ошибка: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return False

def main():
    """Основная функция"""
    print("🔧 АВТОМАТИЧЕСКОЕ ИСПРАВЛЕНИЕ И ТЕСТИРОВАНИЕ")
    print("=" * 60)
    
    # Обновляем репозиторий
    if not update_repository():
        print("❌ Не удалось обновить репозиторий")
        return
    
    print("\n⏳ Ждем 30 секунд для развертывания...")
    time.sleep(30)
    
    # Тестируем изменение логина
    success = test_login_change()
    
    print("\n📋 РЕЗУЛЬТАТ")
    print("=" * 60)
    
    if success:
        print("✅ ТЕСТ ПРОЙДЕН!")
        print("   Логин админа успешно изменен")
    else:
        print("❌ ТЕСТ НЕ ПРОЙДЕН!")
        print("   Есть проблемы с изменением логина")
    
    return success

if __name__ == "__main__":
    main()
