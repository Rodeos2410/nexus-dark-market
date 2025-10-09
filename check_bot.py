#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def check_bot_status():
    """Проверяет статус Telegram бота"""
    
    print("🤖 Проверка статуса Telegram бота")
    print("=" * 50)
    
    bot_token = "8458514538:AAFIAT7BrKelIHie9-JscBnOlAFd_V2qyMY"
    
    # 1. Проверяем информацию о боте
    print("\n1️⃣ Проверка информации о боте:")
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            bot_info = response.json()
            if bot_info.get('ok'):
                print("✅ Бот доступен")
                print(f"🤖 Имя: {bot_info['result']['first_name']}")
                print(f"🆔 Username: @{bot_info['result']['username']}")
                print(f"🆔 ID: {bot_info['result']['id']}")
            else:
                print(f"❌ Ошибка API: {bot_info}")
                return False
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False
    
    # 2. Проверяем webhook
    print("\n2️⃣ Проверка webhook:")
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            webhook_info = response.json()
            if webhook_info.get('ok'):
                result = webhook_info['result']
                print(f"🔗 Webhook URL: {result.get('url', 'Не настроен')}")
                print(f"📊 Ожидающих обновлений: {result.get('pending_update_count', 0)}")
                print(f"❌ Ошибок: {result.get('last_error_message', 'Нет')}")
                
                if result.get('url'):
                    print("✅ Webhook настроен")
                else:
                    print("❌ Webhook не настроен")
                    print("💡 Нужно настроить webhook для работы бота")
                    
            else:
                print(f"❌ Ошибка webhook info: {webhook_info}")
                return False
        else:
            print(f"❌ HTTP ошибка webhook: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка webhook: {e}")
        return False
    
    # 3. Проверяем обновления
    print("\n3️⃣ Проверка обновлений:")
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            updates = response.json()
            if updates.get('ok'):
                update_count = len(updates['result'])
                print(f"📨 Получено обновлений: {update_count}")
                
                if update_count > 0:
                    print("📋 Последние обновления:")
                    for i, update in enumerate(updates['result'][-3:]):  # Показываем последние 3
                        if 'message' in update:
                            msg = update['message']
                            print(f"  {i+1}. Chat ID: {msg['chat']['id']}, Text: {msg.get('text', 'Нет текста')}")
                else:
                    print("📭 Нет новых сообщений")
                    
            else:
                print(f"❌ Ошибка получения обновлений: {updates}")
                return False
        else:
            print(f"❌ HTTP ошибка обновлений: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка обновлений: {e}")
        return False
    
    return True

def main():
    """Основная функция"""
    print("🔍 Диагностика Telegram бота")
    print("=" * 50)
    
    if check_bot_status():
        print("\n✅ Диагностика завершена")
        print("\n💡 Рекомендации:")
        print("1. Если webhook не настроен - настройте его")
        print("2. Если есть ошибки - проверьте URL webhook")
        print("3. Если бот не отвечает - проверьте логи приложения")
    else:
        print("\n❌ Обнаружены проблемы с ботом")
        print("\n💡 Проверьте:")
        print("1. Правильность токена бота")
        print("2. Доступность интернета")
        print("3. Статус Telegram API")

if __name__ == "__main__":
    main()
