#!/usr/bin/env python3
"""
Версия app.py без проверки Telegram для быстрого запуска
"""

# Копируем весь код из app.py, но убираем проверку Telegram
# Это временное решение для запуска приложения

import os
import sys

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Импортируем основной app.py
from app import app

if __name__ == '__main__':
    print("🚀 Запуск Nexus Dark без проверки Telegram...")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
