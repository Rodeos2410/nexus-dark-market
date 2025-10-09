import os
import json
from flask import Flask, request, jsonify
from telegram_bot import process_telegram_update

app = Flask(__name__)

# Получаем токен бота из переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8458514538:AAFIAT7BrKelIHie9-JscBnOlAFd_V2qyMY')

@app.route('/')
def home():
    """Главная страница"""
    return "🤖 Telegram Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    """Обработчик webhook от Telegram"""
    try:
        # Получаем данные от Telegram
        update = request.get_json()
        
        if update:
            # Обрабатываем обновление
            process_telegram_update(update)
            
        return jsonify({'status': 'ok'})
    
    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Устанавливает webhook для бота"""
    try:
        import requests
        
        # Получаем URL приложения
        webhook_url = request.url_root + 'webhook'
        
        # Устанавливаем webhook
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook"
        data = {'url': webhook_url}
        
        response = requests.post(url, data=data)
        result = response.json()
        
        return jsonify({
            'status': 'success',
            'webhook_url': webhook_url,
            'telegram_response': result
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/get_webhook_info', methods=['GET'])
def get_webhook_info():
    """Получает информацию о текущем webhook"""
    try:
        import requests
        
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getWebhookInfo"
        response = requests.get(url)
        result = response.json()
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/delete_webhook', methods=['GET'])
def delete_webhook():
    """Удаляет webhook"""
    try:
        import requests
        
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteWebhook"
        response = requests.post(url)
        result = response.json()
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
