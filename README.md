# 🛒 Nexus Dark Market

Современный интернет-магазин с интеграцией Telegram бота для уведомлений и администрирования.

## 🚀 Возможности

### 👤 Для пользователей:
- ✅ **Регистрация и авторизация** - безопасная система входа
- ✅ **Каталог товаров** - просмотр и поиск товаров
- ✅ **Корзина покупок** - добавление и управление товарами
- ✅ **Профиль пользователя** - управление данными и балансом
- ✅ **Telegram уведомления** - получение уведомлений о продажах
- ✅ **Загрузка изображений** - добавление фото к товарам

### 👑 Для администраторов:
- ✅ **Админ панель** - управление пользователями и товарами
- ✅ **Telegram админ бот** - управление через Telegram
- ✅ **Статистика** - просмотр статистики системы
- ✅ **Управление балансами** - изменение балансов пользователей
- ✅ **Блокировка пользователей** - управление доступом

## 🛠️ Технологии

- **Backend:** Python 3.9, Flask, SQLAlchemy
- **Frontend:** HTML5, CSS3, JavaScript
- **База данных:** SQLite (разработка), PostgreSQL (продакшен)
- **Telegram:** Bot API, Webhook/Polling
- **Хостинг:** Heroku, Railway, VPS

## 📦 Установка

### Локальная разработка:

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/Rodeos2410/nexus-dark-market.git
cd nexus-dark-market
```

2. **Создайте виртуальное окружение:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

3. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

4. **Запустите приложение:**
```bash
python app.py
```

5. **Запустите админский бот (в отдельном терминале):**
```bash
python admin_bot.py
```

### Развертывание на Heroku:

1. **Создайте приложение на Heroku:**
```bash
heroku create nexus-dark-market
```

2. **Настройте переменные окружения:**
```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key
heroku config:set TELEGRAM_BOT_TOKEN=your-bot-token
```

3. **Разверните приложение:**
```bash
git push heroku main
```

4. **Настройте Telegram webhook:**
```bash
curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook" \
     -d "url=https://nexus-dark-market.herokuapp.com/telegram/webhook"
```

## 🤖 Telegram бот

### Для пользователей:
- **@NexusDarkBot** - получение Chat ID и настройка уведомлений
- Команды: `/start` - получить Chat ID

### Для администраторов:
- **Админ панель** - управление системой через Telegram
- Функции: статистика, управление пользователями, изменение балансов

## 📁 Структура проекта

```
nexus-dark-market/
├── app.py                 # Основное приложение Flask
├── admin_bot.py           # Админский Telegram бот
├── config.py              # Конфигурация
├── requirements.txt       # Зависимости Python
├── Procfile              # Конфигурация для Heroku
├── runtime.txt           # Версия Python для Heroku
├── .gitignore            # Игнорируемые файлы
├── templates/            # HTML шаблоны
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── market.html
│   ├── profile.html
│   └── admin.html
├── static/               # Статические файлы
│   ├── css/
│   │   └── style.css
│   └── uploads/          # Загруженные изображения
└── instance/             # База данных SQLite
    └── nexus_dark.db
```

## 🔧 Конфигурация

### Переменные окружения:
- `FLASK_ENV` - окружение (development/production)
- `SECRET_KEY` - секретный ключ Flask
- `TELEGRAM_BOT_TOKEN` - токен Telegram бота
- `ADMIN_CHAT_ID` - Chat ID администратора

### База данных:
- **SQLite** - для разработки (файл `instance/nexus_dark.db`)
- **PostgreSQL** - для продакшена

## 🚀 Запуск

### Основное приложение:
```bash
python app.py
# или
python launch.py
# или
start_app.bat  # Windows
```

### Админский бот:
```bash
python admin_bot.py
# или
start_admin_bot.bat  # Windows
```

## 📱 Использование

### Для пользователей:
1. Зарегистрируйтесь на сайте
2. Добавьте товары в корзину
3. Настройте Telegram уведомления в профиле
4. Получайте уведомления о продажах

### Для администраторов:
1. Войдите как admin (admin/admin123)
2. Используйте админ панель на сайте
3. Или управляйте через Telegram бота

## 🔒 Безопасность

- ✅ Хеширование паролей (Werkzeug)
- ✅ Защита от CSRF
- ✅ Валидация входных данных
- ✅ Безопасная загрузка файлов
- ✅ Ограничение доступа к админ функциям

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи приложения
2. Убедитесь в правильности конфигурации
3. Проверьте подключение к Telegram API

## 📄 Лицензия

Этот проект создан в образовательных целях.

---

**Nexus Dark Market** - современный интернет-магазин с Telegram интеграцией 🛒🤖
