@echo off
chcp 65001 >nul
echo 🚀 Обновление репозитория с живым чатом
echo ==========================================

python update_live_chat.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Ошибка при выполнении скрипта
    echo 💡 Убедитесь, что Python установлен и доступен в PATH
    pause
    exit /b 1
)

echo.
echo ✅ Скрипт выполнен успешно
pause
