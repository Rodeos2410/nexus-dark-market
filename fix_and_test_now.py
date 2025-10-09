#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

def update_repo():
    """Обновляет репозиторий"""
    print("🚀 Обновление репозитория...")
    
    # Добавляем файлы
    success, stdout, stderr = run_command("git add .")
    if not success:
        print(f"❌ Ошибка git add: {stderr}")
        return False
    
    # Коммитим
    success, stdout, stderr = run_command('git commit -m "Fix state management and add debug logging"')
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

def test_login():
    """Тестирует изменение логина"""
    print("\n🧪 Тестирование изменения логина...")
    
    webhook_url = "https://nexus-dark-market.onrender.com/telegram/webhook"
    
    # 1. /start
    print("1. /start")
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
    print("2. Кнопка изменения логина")
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
    print("3. Ввод логина 'testuser123'")
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
        
        if result.get('ok'):
            if 'result' in result and 'text' in result['result']:
                text = result['result']['text']
                print(f"   📱 Сообщение: {text}")
                
                if "❌ Неизвестная команда" in text:
                    print("   ❌ ОШИБКА ВСЕ ЕЩЕ ЕСТЬ!")
                    return False
                elif "✅ Логин админа изменен" in text:
                    print("   ✅ УСПЕХ!")
                    return True
                else:
                    print("   ⚠️ Неожиданный ответ")
                    return False
            else:
                print("   ⚠️ Нет текста")
                return False
        else:
            print("   ❌ Ошибка API")
            return False
    else:
        print("   ❌ HTTP ошибка")
        return False

def main():
    """Основная функция"""
    print("🔧 ИСПРАВЛЕНИЕ И ТЕСТИРОВАНИЕ")
    print("=" * 40)
    
    # Обновляем репозиторий
    if update_repo():
        print("\n⏳ Ждем 30 секунд для развертывания...")
        time.sleep(30)
        
        # Тестируем
        success = test_login()
        
        print(f"\n📋 РЕЗУЛЬТАТ: {'✅ Успех' if success else '❌ Ошибка'}")
        
        if success:
            print("🎉 ОШИБКА ИСПРАВЛЕНА!")
        else:
            print("❌ Ошибка все еще есть")
    else:
        print("❌ Не удалось обновить репозиторий")

if __name__ == "__main__":
    main()
