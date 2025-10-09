import requests
import json

# Тест webhook
print("🧪 Тестируем webhook...")

test_data = {
    "message": {
        "message_id": 999,
        "from": {
            "id": 123456789,
            "username": "test_user"
        },
        "chat": {
            "id": 123456789,
            "type": "private"
        },
        "text": "/start get_id"
    }
}

try:
    response = requests.post(
        'http://localhost:5000/telegram/webhook',
        json=test_data,
        timeout=10
    )
    
    print(f"✅ Webhook статус: {response.status_code}")
    print(f"📊 Ответ: {response.json()}")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")

print("\n🎯 Тест завершен!")
