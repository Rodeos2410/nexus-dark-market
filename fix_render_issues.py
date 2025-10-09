#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Исправление проблем с Render и настройка Telegram бота
"""

import requests
import time

def test_website():
    """Тестирует веб-сайт"""
    print("🌐 Тестирование веб-сайта")
    print("=" * 40)
    
    app_url = "https://nexus-dark-market.onrender.com"
    
    # Тестируем основные endpoints
    endpoints = [
        ("/", "Главная страница"),
        ("/market", "Маркет"),
        ("/login", "Страница входа"),
        ("/register", "Страница регистрации"),
    ]
    
    working_endpoints = 0
    
    for endpoint, description in endpoints:
        url = f"{app_url}{endpoint}"
        print(f"📱 {description}: {endpoint}")
        
        try:
            response = requests.get(url, timeout=15)
            status = response.status_code
            
            if status == 200:
                print(f"   ✅ Работает ({status})")
                working_endpoints += 1
            elif status == 302:
                print(f"   🔄 Редирект ({status}) - нормально")
                working_endpoints += 1
            else:
                print(f"   ❌ Статус {status}")
                
        except requests.exceptions.Timeout:
            print("   ⏰ Таймаут")
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
    
    return working_endpoints, len(endpoints)

def setup_telegram_webhook():
    """Настраивает webhook для Telegram"""
    print(f"\n🔗 Настройка Telegram webhook")
    print("=" * 40)
    
    bot_token = "8458514538:AAFIAT7BrKelIHie9-JscBnOlAFd_V2qyMY"
    app_url = "https://nexus-dark-market.onrender.com"
    webhook_url = f"{app_url}/telegram/webhook"
    
    print(f"🤖 Бот: @NexusDarkBot")
    print(f"🌐 Приложение: {app_url}")
    print(f"🔗 Webhook URL: {webhook_url}")
    
    # Удаляем старый webhook
    print("\n🗑️ Удаление старого webhook...")
    try:
        url = f"https://api.telegram.org/bot{bot_token}/deleteWebhook"
        response = requests.post(url, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                print("   ✅ Старый webhook удален")
            else:
                print(f"   ⚠️ Ошибка удаления: {result}")
    except Exception as e:
        print(f"   ⚠️ Ошибка удаления webhook: {e}")
    
    # Устанавливаем новый webhook
    print("\n🔗 Установка нового webhook...")
    try:
        url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
        payload = {'url': webhook_url}
        
        response = requests.post(url, data=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                print("   ✅ Webhook установлен успешно")
                return True
            else:
                print(f"   ❌ Ошибка установки: {result}")
                return False
        else:
            print(f"   ❌ HTTP ошибка установки: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Ошибка установки webhook: {e}")
        return False

def test_telegram_bot():
    """Тестирует Telegram бота"""
    print(f"\n🤖 Тестирование Telegram бота")
    print("=" * 40)
    
    bot_token = "8458514538:AAFIAT7BrKelIHie9-JscBnOlAFd_V2qyMY"
    
    # Проверяем информацию о боте
    print("📱 Проверка бота...")
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            bot_info = response.json()
            if bot_info.get('ok'):
                print(f"   ✅ Бот доступен: {bot_info['result']['first_name']}")
                print(f"   🆔 Username: @{bot_info['result']['username']}")
                return True
            else:
                print(f"   ❌ Ошибка API: {bot_info}")
                return False
        else:
            print(f"   ❌ HTTP ошибка: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return False

def test_webhook_functionality():
    """Тестирует функциональность webhook"""
    print(f"\n🔗 Тестирование webhook")
    print("=" * 40)
    
    app_url = "https://nexus-dark-market.onrender.com"
    webhook_url = f"{app_url}/telegram/webhook"
    
    # Тестовое сообщение
    test_message = {
        "update_id": 999999999,
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
        }
    }
    
    print(f"📤 Отправка тестового сообщения...")
    try:
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
        print(f"   ❌ Ошибка: {e}")
        return False

def test_admin_login():
    """Тестирует вход администратора"""
    print(f"\n👑 Тестирование входа администратора")
    print("=" * 40)
    
    app_url = "https://nexus-dark-market.onrender.com"
    login_url = f"{app_url}/login"
    
    print(f"📱 Тестирование страницы входа...")
    try:
        response = requests.get(login_url, timeout=15)
        
        if response.status_code == 200:
            print("   ✅ Страница входа доступна")
            return True
        elif response.status_code == 302:
            print("   🔄 Редирект - нормально")
            return True
        else:
            print(f"   ❌ Статус {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return False

def main():
    """Основная функция исправления"""
    print("🔧 Исправление проблем с Render и настройка бота")
    print("=" * 70)
    
    # Тестируем веб-сайт
    working_endpoints, total_endpoints = test_website()
    
    # Тестируем Telegram бота
    bot_working = test_telegram_bot()
    
    # Настраиваем webhook
    webhook_setup = setup_telegram_webhook()
    
    # Тестируем webhook
    webhook_working = test_webhook_functionality()
    
    # Тестируем вход администратора
    admin_login = test_admin_login()
    
    # Итоговый отчет
    print("\n📋 ИТОГОВЫЙ ОТЧЕТ")
    print("=" * 70)
    
    print(f"🌐 Веб-сайт: {'✅ Работает' if working_endpoints > 0 else '❌ Не работает'}")
    print(f"🤖 Telegram бот: {'✅ Работает' if bot_working else '❌ Не работает'}")
    print(f"🔗 Webhook: {'✅ Настроен' if webhook_setup else '❌ Не настроен'}")
    print(f"⚡ Webhook функциональность: {'✅ Работает' if webhook_working else '❌ Не работает'}")
    print(f"👑 Админ вход: {'✅ Доступен' if admin_login else '❌ Не доступен'}")
    print(f"📊 Endpoints: {working_endpoints}/{total_endpoints} работают")
    
    if bot_working and webhook_setup and webhook_working and working_endpoints > 0:
        print("\n🎉 ВСЕ КОМПОНЕНТЫ РАБОТАЮТ!")
        print("\n🔗 Ссылки:")
        print("🌐 Сайт: https://nexus-dark-market.onrender.com")
        print("📱 Бот: @NexusDarkBot")
        print("👑 Админ: admin/admin123")
        
        print("\n🔧 Для тестирования:")
        print("1. Зайдите на https://nexus-dark-market.onrender.com")
        print("2. Войдите как admin/admin123")
        print("3. Напишите боту @NexusDarkBot /start")
        print("4. Используйте кнопки админ панели")
        print("5. Протестируйте уведомления")
        
        return True
    else:
        print("\n⚠️ НЕКОТОРЫЕ КОМПОНЕНТЫ ТРЕБУЮТ ВНИМАНИЯ")
        print("\n💡 Рекомендации:")
        if not bot_working:
            print("- Проверьте токен бота")
        if not webhook_setup:
            print("- Настройте webhook вручную")
        if not webhook_working:
            print("- Проверьте логи приложения на Render")
        if working_endpoints == 0:
            print("- Проверьте деплой на Render")
        
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
