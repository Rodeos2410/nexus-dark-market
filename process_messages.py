#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

def process_pending_messages():
    """Обрабатывает накопившиеся сообщения"""
    
    print("📨 Обработка накопившихся сообщений")
    print("=" * 50)
    
    bot_token = "8458514538:AAFIAT7BrKelIHie9-JscBnOlAFd_V2qyMY"
    
    # Получаем обновления
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"❌ Ошибка получения обновлений: {response.status_code}")
        return
    
    updates = response.json()
    if not updates.get('ok'):
        print(f"❌ Ошибка API: {updates}")
        return
    
    messages = updates['result']
    print(f"📊 Найдено сообщений: {len(messages)}")
    
    if not messages:
        print("✅ Нет сообщений для обработки")
        return
    
    # Обрабатываем каждое сообщение
    for i, update in enumerate(messages):
        if 'message' in update:
            message = update['message']
            chat_id = str(message['chat']['id'])
            text = message.get('text', '')
            username = message['from'].get('username', '')
            
            print(f"\n📱 Сообщение {i+1}:")
            print(f"   Chat ID: {chat_id}")
            print(f"   Username: @{username}")
            print(f"   Text: {text}")
            
            # Отправляем ответ
            if text.startswith('/start'):
                if chat_id == '1172834372':  # Админ
                    response_text = "👋 Привет, админ! Бот работает в режиме polling."
                else:
                    response_text = f"""🆔 <b>Ваш Chat ID:</b>

<code>{chat_id}</code>

📋 <b>Как скопировать:</b>
• Нажмите на ID выше
• Или выделите и скопируйте вручную

🔧 <b>Что дальше:</b>
1. Скопируйте этот ID
2. Вставьте в поле на сайте Nexus Dark
3. Нажмите 'Настроить'

✅ <b>Готово!</b> Вы будете получать уведомления о продажах ваших товаров."""
            else:
                response_text = f"""🆔 <b>Ваш Chat ID:</b>

<code>{chat_id}</code>

📋 <b>Как скопировать:</b>
• Нажмите на ID выше
• Или выделите и скопируйте вручную

🔧 <b>Что дальше:</b>
1. Скопируйте этот ID
2. Вставьте в поле на сайте Nexus Dark
3. Нажмите 'Настроить'

✅ <b>Готово!</b> Вы будете получать уведомления о продажах ваших товаров."""
            
            # Отправляем ответ
            send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            send_data = {
                'chat_id': chat_id,
                'text': response_text,
                'parse_mode': 'HTML'
            }
            
            send_response = requests.post(send_url, json=send_data)
            if send_response.status_code == 200:
                print(f"   ✅ Ответ отправлен")
            else:
                print(f"   ❌ Ошибка отправки: {send_response.status_code}")
            
            time.sleep(0.5)  # Небольшая задержка между сообщениями
    
    print(f"\n✅ Обработано {len(messages)} сообщений")
    print("\n💡 Теперь бот будет отвечать на новые сообщения")

if __name__ == "__main__":
    process_pending_messages()
