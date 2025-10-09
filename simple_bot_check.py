import requests

print("🤖 Проверка Telegram бота")
print("=" * 40)

bot_token = "8458514538:AAFIAT7BrKelIHie9-JscBnOlAFd_V2qyMY"

# Проверяем информацию о боте
print("\n1️⃣ Проверка бота:")
try:
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    response = requests.get(url, timeout=10)
    
    if response.status_code == 200:
        bot_info = response.json()
        if bot_info.get('ok'):
            print("✅ Бот доступен")
            print(f"🤖 Имя: {bot_info['result']['first_name']}")
            print(f"🆔 Username: @{bot_info['result']['username']}")
        else:
            print(f"❌ Ошибка API: {bot_info}")
    else:
        print(f"❌ HTTP ошибка: {response.status_code}")
        
except Exception as e:
    print(f"❌ Ошибка: {e}")

# Проверяем webhook
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
            
            if result.get('url'):
                print("✅ Webhook настроен")
            else:
                print("❌ Webhook не настроен")
        else:
            print(f"❌ Ошибка: {webhook_info}")
    else:
        print(f"❌ HTTP ошибка: {response.status_code}")
        
except Exception as e:
    print(f"❌ Ошибка: {e}")

print("\n💡 Если webhook не настроен, настройте его командой:")
print("curl -X POST \"https://api.telegram.org/bot8458514538:AAFIAT7BrKelIHie9-JscBnOlAFd_V2qyMY/setWebhook\" -d \"url=https://ВАШ-URL/telegram/webhook\"")
