#!/usr/bin/env python3
"""
Скрипт для исправления проблем с Telegram токеном
"""

import os
import requests
import json

def check_telegram_token():
    """Проверяет валидность Telegram токена"""
    token = os.environ.get('TELEGRAM_BOT_TOKEN', '8458514538:AAEQruDKFmiEwRlMS-MmtUJ6D6vF2VOQ9Sc')
    
    print(f"🔍 Проверяем токен: {token[:10]}...")
    
    try:
        url = f"https://api.telegram.org/bot{token}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data.get('result', {})
                print(f"✅ Токен валиден!")
                print(f"🤖 Имя бота: {bot_info.get('first_name', 'N/A')}")
                print(f"🆔 Username: @{bot_info.get('username', 'N/A')}")
                print(f"🆔 ID: {bot_info.get('id', 'N/A')}")
                return True
            else:
                print(f"❌ Ошибка API: {data}")
                return False
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            print(f"📄 Ответ: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

def test_telegram_send():
    """Тестирует отправку сообщения"""
    token = os.environ.get('TELEGRAM_BOT_TOKEN', '8458514538:AAEQruDKFmiEwRlMS-MmtUJ6D6vF2VOQ9Sc')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID', '1172834372')
    
    print(f"📱 Тестируем отправку в chat_id: {chat_id}")
    
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': '🧪 Тестовое сообщение от Nexus Dark',
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, data=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                print(f"✅ Сообщение отправлено успешно!")
                return True
            else:
                print(f"❌ Ошибка отправки: {data}")
                return False
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            print(f"📄 Ответ: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")
        return False

def main():
    print("🚀 Проверка Telegram токена...")
    print("=" * 50)
    
    # Проверяем переменные окружения
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    print(f"🔧 TELEGRAM_BOT_TOKEN: {'✅ Установлен' if token else '❌ Не установлен'}")
    print(f"🔧 TELEGRAM_CHAT_ID: {'✅ Установлен' if chat_id else '❌ Не установлен'}")
    
    if not token:
        print("⚠️ Используем токен по умолчанию")
    
    print("\n" + "=" * 50)
    
    # Проверяем токен
    if check_telegram_token():
        print("\n" + "=" * 50)
        # Тестируем отправку
        test_telegram_send()
    else:
        print("\n❌ Токен невалиден. Проверьте настройки.")
    
    print("\n" + "=" * 50)
    print("🏁 Проверка завершена")

if __name__ == "__main__":
    main()
