@echo off
chcp 65001 >nul
echo Проверка базы данных...
cd /d "%~dp0"
python debug_db.py
pause


