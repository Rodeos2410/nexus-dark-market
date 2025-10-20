@echo off
chcp 65001 >nul
echo 🧪 Добавление простого чата для тестирования
echo ============================================

python add_simple_chat.py

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
