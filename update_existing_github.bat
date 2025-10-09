@echo off
chcp 65001 >nul
echo 🔄 Обновление существующего репозитория на GitHub
echo ====================================================
echo 🎯 Цель: https://github.com/Rodeos2410/nexus-dark-market.git
echo.

echo 🔧 Настройка Git репозитория...
if not exist .git (
    echo 📁 Инициализация Git репозитория...
    git init
    if %errorlevel% neq 0 (
        echo ❌ Ошибка инициализации Git
        pause
        exit /b 1
    )
)

echo 🔗 Настройка удаленного репозитория...
git remote remove origin 2>nul
git remote add origin https://github.com/Rodeos2410/nexus-dark-market.git
if %errorlevel% neq 0 (
    echo ❌ Ошибка настройки remote
    pause
    exit /b 1
)

echo 📡 Проверка remote...
git remote -v

echo.
echo 📁 Принудительное обновление файлов...
git add -A
if %errorlevel% neq 0 (
    echo ❌ Ошибка добавления файлов
    pause
    exit /b 1
)

echo 📊 Проверка статуса...
git status

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
echo 🚀 Принудительная отправка в GitHub...
git push -f origin main
if %errorlevel% neq 0 (
    echo ❌ Ошибка отправки в GitHub
    pause
    exit /b 1
)

echo.
echo 🎉 РЕПОЗИТОРИЙ УСПЕШНО ОБНОВЛЕН!
echo ====================================================
echo.
echo 📋 Что сделано:
echo ✅ Git репозиторий настроен
echo ✅ Все файлы обновлены
echo ✅ Создан коммит с описанием
echo ✅ Изменения отправлены в GitHub
echo.
echo 🔗 Проверьте репозиторий:
echo https://github.com/Rodeos2410/nexus-dark-market
echo.
echo 🔧 Следующие шаги:
echo 1. Обновите деплой на Render
echo 2. Запустите: python setup_webhook.py
echo 3. Протестируйте: python test_all_components.py
echo.
pause
