#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диагностика проблем с ботом
"""

import requests
import json
import time

def check_website():
    """Проверяет доступность сайта"""
    print("🌐 Проверка сайта...")
    try:
        response = requests.get("https://nexus-dark-market.onrender.com", timeout=10)
        if response.status_code == 200:
            print("   ✅ Сайт доступен")
            return True
        else:
            print(f"   ❌ Сайт недоступен: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Ошибка подключения к сайту: {e}")
        return False

def check_webhook():
    """Проверяет статус webhook"""
    print("\n🔗 Проверка webhook...")
    try:
        bot_token = "8458514538:AAFIAT7BrKelIHie9-JscBnOlAFd_V2qyMY"
        url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                webhook_info = data.get('result', {})
                webhook_url = webhook_info.get('url', '')
                pending_updates = webhook_info.get('pending_update_count', 0)
                
                print(f"   📍 Webhook URL: {webhook_url}")
                print(f"   📊 Ожидающих обновлений: {pending_updates}")
                
                if webhook_url:
                    print("   ✅ Webhook настроен")
                    return True
                else:
                    print("   ❌ Webhook не настроен")
                    return False
            else:
                print(f"   ❌ Ошибка API: {data}")
                return False
        else:
            print(f"   ❌ HTTP ошибка: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Ошибка проверки webhook: {e}")
        return False

def test_webhook():
    """Тестирует webhook"""
    print("\n🧪 Тестирование webhook...")
    try:
        webhook_url = "https://nexus-dark-market.onrender.com/telegram/webhook"
        
        # Создаем тестовое сообщение
        test_message = {
            "update_id": int(time.time()),
            "message": {
                "message_id": int(time.time()),
                "from": {
                    "id": 1172834372,
                    "is_bot": False,
                    "first_name": "Test",
                    "username": "test_admin"
                },
                "chat": {
                    "id": 1172834372,
                    "first_name": "Test",
                    "username": "test_admin",
                    "type": "private"
                },
                "date": int(time.time()),
                "text": "/start"
            }
        }
        
        response = requests.post(webhook_url, json=test_message, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                print("   ✅ Webhook работает")
                return True
            else:
                print(f"   ❌ Ошибка webhook: {result}")
                return False
        else:
            print(f"   ❌ HTTP ошибка: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Ошибка тестирования webhook: {e}")
        return False

def test_bot_commands():
    """Тестирует команды бота"""
    print("\n🤖 Тестирование команд бота...")
    
    commands_to_test = [
        "/start",
        "stats",
        "users",
        "management",
        "telegram",
        "admin_settings",
        "help"
    ]
    
    webhook_url = "https://nexus-dark-market.onrender.com/telegram/webhook"
    
    for command in commands_to_test:
        print(f"   📱 Тестирование: {command}")
        
        # Создаем тестовое сообщение
        test_message = {
            "update_id": int(time.time()),
            "message": {
                "message_id": int(time.time()),
                "from": {
                    "id": 1172834372,
                    "is_bot": False,
                    "first_name": "Test",
                    "username": "test_admin"
                },
                "chat": {
                    "id": 1172834372,
                    "first_name": "Test",
                    "username": "test_admin",
                    "type": "private"
                },
                "date": int(time.time()),
                "text": command
            }
        }
        
        try:
            response = requests.post(webhook_url, json=test_message, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    print(f"      ✅ {command} - работает")
                else:
                    print(f"      ❌ {command} - ошибка: {result}")
            else:
                print(f"      ❌ {command} - HTTP ошибка: {response.status_code}")
                
        except Exception as e:
            print(f"      ❌ {command} - ошибка: {e}")
        
        time.sleep(1)  # Пауза между запросами

def test_callback_queries():
    """Тестирует callback запросы"""
    print("\n🔘 Тестирование callback запросов...")
    
    callbacks_to_test = [
        "stats",
        "users",
        "management",
        "telegram",
        "admin_settings",
        "change_admin_username",
        "change_admin_password",
        "admin_info",
        "help",
        "main_menu"
    ]
    
    webhook_url = "https://nexus-dark-market.onrender.com/telegram/webhook"
    
    for callback in callbacks_to_test:
        print(f"   🔘 Тестирование: {callback}")
        
        # Создаем тестовый callback запрос
        callback_query = {
            "id": f"test_{int(time.time())}",
            "from": {
                "id": 1172834372,
                "is_bot": False,
                "first_name": "Test",
                "username": "test_admin"
            },
            "message": {
                "message_id": 1,
                "from": {
                    "id": 1172834372,
                    "is_bot": False,
                    "first_name": "Test",
                    "username": "test_admin"
                },
                "chat": {
                    "id": 1172834372,
                    "first_name": "Test",
                    "username": "test_admin",
                    "type": "private"
                },
                "date": int(time.time()),
                "text": "/start"
            },
            "data": callback
        }
        
        webhook_data = {
            "update_id": int(time.time()),
            "callback_query": callback_query
        }
        
        try:
            response = requests.post(webhook_url, json=webhook_data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    print(f"      ✅ {callback} - работает")
                else:
                    print(f"      ❌ {callback} - ошибка: {result}")
            else:
                print(f"      ❌ {callback} - HTTP ошибка: {response.status_code}")
                
        except Exception as e:
            print(f"      ❌ {callback} - ошибка: {e}")
        
        time.sleep(1)  # Пауза между запросами

def setup_webhook():
    """Настраивает webhook"""
    print("\n🔧 Настройка webhook...")
    try:
        bot_token = "8458514538:AAFIAT7BrKelIHie9-JscBnOlAFd_V2qyMY"
        webhook_url = "https://nexus-dark-market.onrender.com/telegram/webhook"
        
        url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
        data = {"url": webhook_url}
        
        response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                print("   ✅ Webhook настроен успешно")
                return True
            else:
                print(f"   ❌ Ошибка настройки webhook: {result}")
                return False
        else:
            print(f"   ❌ HTTP ошибка: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Ошибка настройки webhook: {e}")
        return False

def main():
    """Основная функция диагностики"""
    print("🔍 ДИАГНОСТИКА ПРОБЛЕМ С БОТОМ")
    print("=" * 50)
    
    # Проверяем сайт
    website_ok = check_website()
    
    # Проверяем webhook
    webhook_ok = check_webhook()
    
    # Если webhook не настроен, настраиваем его
    if not webhook_ok:
        print("\n🔧 Webhook не настроен, настраиваем...")
        webhook_ok = setup_webhook()
    
    # Тестируем webhook
    if webhook_ok:
        test_webhook()
    
    # Тестируем команды бота
    if website_ok:
        test_bot_commands()
    
    # Тестируем callback запросы
    if website_ok:
        test_callback_queries()
    
    print("\n📋 ИТОГОВЫЙ ОТЧЕТ")
    print("=" * 50)
    
    if website_ok and webhook_ok:
        print("✅ Все компоненты работают!")
        print("   • Сайт доступен")
        print("   • Webhook настроен")
        print("   • Бот должен работать")
        
        print("\n💡 Для тестирования:")
        print("   1. Напишите боту @NexusDarkBot /start")
        print("   2. Проверьте все кнопки")
        print("   3. Попробуйте изменить логин и пароль")
        
    else:
        print("❌ Обнаружены проблемы:")
        if not website_ok:
            print("   • Сайт недоступен")
        if not webhook_ok:
            print("   • Webhook не настроен")
        
        print("\n🔧 Рекомендации:")
        print("   1. Проверьте статус развертывания на Render")
        print("   2. Убедитесь, что все переменные окружения настроены")
        print("   3. Проверьте логи приложения")

if __name__ == "__main__":
    main()
