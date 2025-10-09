#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

def test_webhook():
    """Простой тест webhook"""
    print("🧪 Простой тест webhook")
    
    webhook_url = "https://nexus-dark-market.onrender.com/telegram/webhook"
    
    # Тест 1: Отправляем /start
    print("1. Тестируем /start...")
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
    
    try:
        response = requests.post(webhook_url, json=message, timeout=10)
        print(f"   Статус: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ /start работает")
        else:
            print(f"   ❌ Ошибка: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    time.sleep(1)
    
    # Тест 2: Нажимаем кнопку изменения логина
    print("\n2. Тестируем кнопку изменения логина...")
    callback = {
        "update_id": 2,
        "callback_query": {
            "id": "test_callback",
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
        if response.status_code == 200:
            print("   ✅ Кнопка изменения логина работает")
        else:
            print(f"   ❌ Ошибка: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    time.sleep(1)
    
    # Тест 3: Вводим новый логин
    print("\n3. Тестируем ввод нового логина...")
    message = {
        "update_id": 3,
        "message": {
            "message_id": 2,
            "from": {"id": 1172834372, "is_bot": False, "first_name": "Test"},
            "chat": {"id": 1172834372, "type": "private"},
            "date": int(time.time()),
            "text": "newadmin123"
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

if __name__ == "__main__":
    print("🚀 ПРОСТОЙ ТЕСТ WEBHOOK")
    print("=" * 40)
    
    success = test_webhook()
    
    print("\n📋 РЕЗУЛЬТАТ")
    print("=" * 40)
    
    if success:
        print("✅ ТЕСТ ПРОЙДЕН!")
    else:
        print("❌ ТЕСТ НЕ ПРОЙДЕН!")
