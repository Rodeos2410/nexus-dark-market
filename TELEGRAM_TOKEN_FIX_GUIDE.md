# 🔧 Исправление ошибки 401 в Telegram боте

## ❌ Проблема
```
❌ HTTP ошибка: 401
❌ Ошибка подключения к Telegram
```

## 🔍 Диагностика
Токен бота `8458514538:AAFIAT7BrKelIHie9-JscBnOlAFd_V2qyMY` неверный или истек.

## ✅ Решение

### 1. Создайте нового бота через @BotFather

1. Откройте Telegram и найдите @BotFather
2. Отправьте команду `/newbot`
3. Введите имя бота (например: "Nexus Dark Market Bot")
4. Введите username бота (например: "nexus_dark_market_bot")
5. Скопируйте полученный токен

### 2. Обновите токен в коде

Замените токен в файлах:

**В `app.py` (строка 98):**
```python
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'ВАШ_НОВЫЙ_ТОКЕН_ЗДЕСЬ')
```

**В `telegram_bot.py` (строка 9):**
```python
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'ВАШ_НОВЫЙ_ТОКЕН_ЗДЕСЬ')
```

### 3. Обновите переменные окружения на Render

1. Зайдите в панель управления Render
2. Выберите ваш проект
3. Перейдите в раздел "Environment"
4. Обновите переменную `TELEGRAM_BOT_TOKEN` на новый токен
5. Сохраните изменения

### 4. Перезапустите приложение

После обновления токена перезапустите приложение на Render.

## 🧪 Тестирование

После обновления токена протестируйте:

```python
import requests

token = "ВАШ_НОВЫЙ_ТОКЕН"
response = requests.get(f"https://api.telegram.org/bot{token}/getMe")
print(response.json())
```

Должен вернуть:
```json
{
  "ok": true,
  "result": {
    "id": 123456789,
    "is_bot": true,
    "first_name": "Nexus Dark Market Bot",
    "username": "nexus_dark_market_bot"
  }
}
```

## 📝 Важные замечания

- Никогда не публикуйте токен бота в открытом доступе
- Используйте переменные окружения для хранения токенов
- Регулярно проверяйте работоспособность бота
- При необходимости создавайте новый токен через @BotFather

## 🔗 Полезные ссылки

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [@BotFather](https://t.me/BotFather)
- [Render Environment Variables](https://render.com/docs/environment-variables)
