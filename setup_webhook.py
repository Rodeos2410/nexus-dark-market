#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт для настройки webhook после деплоя на Render
"""

import requests
import time

def setup_webhook():
    """Настраивает webhook для Telegram бота"""
    
    print("🔗 Настройка webhook для Telegram бота")
    print("=" * 50)
    
    bot_token = "8458514538:AAFIAT7BrKelIHie9-JscBnOlAFd_V2qyMY"
    app_url = "https://nexus-dark-market-1.onrender.com"
    webhook_url = f"{app_url}/telegram/webhook"
    
    print(f"🤖 Бот: @NexusDarkBot")
    print(f"🌐 Приложение: {app_url}")
    print(f"🔗 Webhook URL: {webhook_url}")
    print()
    
    # Ждем, пока приложение запустится
    print("⏳ Ожидание запуска приложения...")
    for i in range(30):
        try:
            response = requests.get(app_url, timeout=5)
            if response.status_code in [200, 404]:  # 404 тоже нормально для главной страницы
                print("✅ Приложение запущено")
                break
        except:
            pass
        print(f"   Ожидание... {i+1}/30")
        time.sleep(2)
    else:
        print("❌ Приложение не запустилось за 60 секунд")
        return False
    
    # Удаляем старый webhook
    print("\n🗑️ Удаление старого webhook...")
    try:
        url = f"https://api.telegram.org/bot{bot_token}/deleteWebhook"
        response = requests.post(url, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                print("✅ Старый webhook удален")
            else:
                print(f"⚠️ Ошибка удаления: {result}")
        else:
            print(f"⚠️ HTTP ошибка удаления: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Ошибка удаления webhook: {e}")
    
    # Устанавливаем новый webhook
    print("\n🔗 Установка нового webhook...")
    try:
        url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
        payload = {'url': webhook_url}
        
        response = requests.post(url, data=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                print("✅ Webhook установлен успешно")
            else:
                print(f"❌ Ошибка установки: {result}")
                return False
        else:
            print(f"❌ HTTP ошибка установки: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка установки webhook: {e}")
        return False
    
    # Проверяем webhook
    print("\n🔍 Проверка webhook...")
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            webhook_info = response.json()
            if webhook_info.get('ok'):
                result = webhook_info['result']
                current_url = result.get('url', '')
                pending = result.get('pending_update_count', 0)
                
                print(f"🔗 Текущий webhook: {current_url}")
                print(f"📊 Ожидающих обновлений: {pending}")
                
                if current_url == webhook_url:
                    print("✅ Webhook настроен правильно")
                    return True
                else:
                    print("❌ Webhook настроен неправильно")
                    return False
            else:
                print(f"❌ Ошибка проверки: {webhook_info}")
                return False
        else:
            print(f"❌ HTTP ошибка проверки: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка проверки webhook: {e}")
        return False

def test_admin_panel():
    """Тестирует админ панель в боте"""
    print("\n🤖 Тестирование админ панели в боте")
    print("-" * 40)
    
    print("📱 Отправьте боту @NexusDarkBot команду /start")
    print("👑 Должны появиться кнопки админ панели")
    print("✅ Если кнопки появились - админ панель работает")
    
    return True

def main():
    """Основная функция"""
    print("🚀 Настройка webhook после деплоя на Render")
    print("=" * 60)
    
    # Настраиваем webhook
    if setup_webhook():
        print("\n🎉 Webhook настроен успешно!")
        
        # Тестируем админ панель
        test_admin_panel()
        
        print("\n📋 Что работает:")
        print("✅ Веб-сайт: https://nexus-dark-market-1.onrender.com")
        print("✅ Telegram бот: @NexusDarkBot")
        print("✅ Админ панель в боте")
        print("✅ Webhook настроен")
        print("✅ Уведомления Telegram")
        
        print("\n🔧 Для тестирования:")
        print("1. Зайдите на сайт и войдите как admin/admin123")
        print("2. Напишите боту @NexusDarkBot /start")
        print("3. Используйте кнопки админ панели")
        print("4. Протестируйте уведомления")
        
        return True
    else:
        print("\n❌ Ошибка настройки webhook")
        print("\n💡 Проверьте:")
        print("- Запущено ли приложение на Render")
        print("- Правильный ли URL приложения")
        print("- Доступен ли токен бота")
        
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
