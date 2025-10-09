import requests
import time

BOT_TOKEN = '8458514538:AAFIAT7BrKelIHie9-JscBnOlAFd_V2qyMY'
BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'

def send_message(chat_id, text):
    url = f'{BASE_URL}/sendMessage'
    data = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
    response = requests.post(url, data=data, timeout=10)
    return response.json()

def get_updates(offset=None):
    url = f'{BASE_URL}/getUpdates'
    params = {'timeout': 30}
    if offset:
        params['offset'] = offset
    response = requests.get(url, params=params, timeout=35)
    return response.json()

print("🤖 Запуск минимального бота...")
print("⏹️  Для остановки нажмите Ctrl+C")

last_update_id = None

try:
    while True:
        updates = get_updates(last_update_id)
        
        if updates.get('ok'):
            for update in updates.get('result', []):
                last_update_id = update['update_id'] + 1
                
                if 'message' in update:
                    message = update['message']
                    chat_id = message['chat']['id']
                    text = message.get('text', '')
                    username = message['from'].get('username', '')
                    
                    print(f"📱 Получено: {text} от @{username}")
                    
                    # Отправляем Chat ID
                    response = f"""🆔 Ваш Chat ID:

{chat_id}

Скопируйте этот ID и вставьте на сайте Nexus Dark для настройки уведомлений."""
                    
                    result = send_message(chat_id, response)
                    if result.get('ok'):
                        print(f"✅ Ответ отправлен в чат {chat_id}")
                    else:
                        print(f"❌ Ошибка отправки: {result}")
        
        time.sleep(1)

except KeyboardInterrupt:
    print("\n🛑 Бот остановлен")
except Exception as e:
    print(f"❌ Ошибка: {e}")
