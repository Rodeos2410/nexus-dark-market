@echo off
chcp 65001 >nul
echo 🔄 Обновление репозитория на GitHub
echo =====================================

echo.
echo 📋 Проверка Git статуса...
git status
if %errorlevel% neq 0 (
    echo ❌ Git не инициализирован или есть ошибки
    echo 💡 Инициализируйте Git: git init
    pause
    exit /b 1
)

echo.
echo 📁 Добавление всех файлов...
git add .
if %errorlevel% neq 0 (
    echo ❌ Ошибка добавления файлов
    pause
    exit /b 1
)

echo.
echo 💾 Создание коммита...
git commit -m "Complete admin panel with buttons and Render deployment setup

- Added full admin panel with inline buttons in Telegram bot
- Fixed webhook to handle callback queries  
- Updated requirements.txt with all dependencies
- Fixed Procfile for Render deployment
- Added render.yaml with environment variables
- Created initialization scripts for Render
- Added comprehensive testing scripts
- Updated app.py with callback handling
- All components ready for production deployment"

if %errorlevel% neq 0 (
    echo ❌ Ошибка создания коммита
    pause
    exit /b 1
)

echo.
echo 🚀 Отправка в GitHub...
git push origin main
if %errorlevel% neq 0 (
    echo ❌ Ошибка отправки в GitHub
    echo 💡 Попробуйте: git push -u origin main
    pause
    exit /b 1
)

echo.
echo 🎉 РЕПОЗИТОРИЙ УСПЕШНО ОБНОВЛЕН!
echo =====================================
echo.
echo 📋 Что сделано:
echo ✅ Все файлы добавлены в Git
echo ✅ Создан коммит с описанием  
echo ✅ Изменения отправлены в GitHub
echo.
echo 🔧 Следующие шаги:
echo 1. Зайдите на GitHub и проверьте файлы
echo 2. Обновите деплой на Render
echo 3. Запустите: python setup_webhook.py
echo 4. Протестируйте: python test_all_components.py
echo.
echo 🔗 Проверьте ваш репозиторий на GitHub!
echo.
pause
