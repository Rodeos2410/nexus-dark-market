#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

def quick_test():
    """Быстрый тест изменения логина"""
    print("🧪 Быстрый тест изменения логина")
    
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
    print("3. Ввод логина")
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
    response = requests.post(webhook_url, json=message, timeout=5)
    print(f"   Статус: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Ответ: {result}")
        return result.get('ok', False)
    return False

if __name__ == "__main__":
    success = quick_test()
    print(f"\nРезультат: {'✅ Успех' if success else '❌ Ошибка'}")