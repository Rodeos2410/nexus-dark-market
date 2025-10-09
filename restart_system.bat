@echo off
chcp 65001
echo 🚀 Перезапуск системы Nexus Dark Market
echo.

echo 🛑 Останавливаем все процессы Python...
taskkill /f /im python.exe 2>nul

echo.
echo 🗑️ Удаляем старую базу данных...
if exist "instance\nexus_dark.db" del "instance\nexus_dark.db"

echo.
echo 🔄 Создаем новую базу данных...
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('✅ База данных создана')"

echo.
echo 🚀 Запускаем основное приложение...
start "Nexus Dark Market" python app.py

echo.
echo 🤖 Запускаем админский бот...
start "Admin Bot" python admin_bot.py

echo.
echo ✅ Система запущена!
echo 📱 Основное приложение: http://localhost:5000
echo 🤖 Админский бот: работает в фоне
echo.
pause
