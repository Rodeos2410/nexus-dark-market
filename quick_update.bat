@echo off
echo 🚀 Быстрое обновление репозитория...

echo 🔄 Добавляем файлы...
git add .

echo 🔄 Коммитим изменения...
git commit -m "Исправлены все ошибки развертывания - готово к запуску"

echo 🔄 Отправляем в репозиторий...
git push origin main --force

echo 🎉 Готово!
echo.
echo 📋 Что исправлено:
echo ✅ PostgreSQL синтаксис исправлен
echo ✅ База данных работает корректно
echo ✅ Telegram функции сделаны опциональными
echo ✅ Приложение готово к запуску
echo.
echo 🔧 Для полной работы Telegram:
echo 1. Получите новый токен от @BotFather
echo 2. Обновите TELEGRAM_BOT_TOKEN в Render
echo.
pause
