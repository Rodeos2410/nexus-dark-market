#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time

# Конфигурация бота
BOT_TOKEN = '8458514538:AAFIAT7BrKelIHie9-JscBnOlAFd_V2qyMY'
BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'

def send_message(chat_id, text):
    """Отправляет сообщение пользователю"""
    url = f'{BASE_URL}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, data=data, timeout=10)
        result = response.json()
        
        if result.get('ok'):
            print(f"✅ Сообщение отправлено в чат {chat_id}")
            return True
        else:
            print(f"❌ Ошибка отправки: {result.get('description')}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def get_updates(offset=None):
    """Получает обновления от Telegram"""
    url = f'{BASE_URL}/getUpdates'
    params = {'timeout': 30}
    
    if offset:
        params['offset'] = offset
    
    try:
        response = requests.get(url, params=params, timeout=35)
        result = response.json()
        
        if result.get('ok'):
            return result.get('result', [])
        else:
            print(f"❌ Ошибка получения обновлений: {result.get('description')}")
            return []
            
    except Exception as e:
        print(f"❌ Ошибка получения обновлений: {e}")
        return []

def main():
    """Основной цикл бота"""
    print("🤖 Запуск простого Telegram бота...")
    print(f"🔑 Токен: {BOT_TOKEN[:10]}...")
    print("📱 Бот будет отправлять Chat ID при любом сообщении")
    print("⏹️  Для остановки нажмите Ctrl+C")
    print("=" * 50)
    
    last_update_id = None
    
    while True:
        try:
            # Получаем обновления
            updates = get_updates(last_update_id)
            
            for update in updates:
                last_update_id = update['update_id'] + 1
                
                if 'message' in update:
                    message = update['message']
                    chat_id = message['chat']['id']
                    user_id = message['from']['id']
                    username = message['from'].get('username', '')
                    first_name = message['from'].get('first_name', '')
                    text = message.get('text', '')
                    
                    print(f"📱 Получено сообщение от {first_name} (@{username}): {text}")
                    
                    # Отправляем Chat ID с инструкциями
                    id_message = f"""🆔 <b>Ваш Chat ID:</b>

<code>{chat_id}</code>

📋 <b>Как скопировать:</b>
• Нажмите на ID выше
• Или выделите и скопируйте вручную

🔧 <b>Что дальше:</b>
1. Скопируйте этот ID
2. Вставьте в поле на сайте Nexus Dark
3. Нажмите 'Настроить'

✅ <b>Готово!</b> Вы будете получать уведомления о продажах ваших товаров.

💡 <b>Команды:</b>
/start - Получить Chat ID"""
                    
                    send_message(chat_id, id_message)
            
            # Небольшая пауза между запросами
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\n🛑 Бот остановлен пользователем")
            break
        except Exception as e:
            print(f"❌ Ошибка в основном цикле: {e}")
            time.sleep(5)  # Пауза при ошибке

if __name__ == "__main__":
    main()
