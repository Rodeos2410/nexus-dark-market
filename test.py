#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

print("Тестирование импорта приложения...")
print(f"Текущая директория: {os.getcwd()}")

try:
    print("Импортируем app...")
    from app import app
    print("Импорт успешен!")
    print("Запускаем приложение...")
    app.run(debug=True, host='0.0.0.0', port=5000)
except Exception as e:
    print(f"Ошибка: {e}")
    import traceback
    traceback.print_exc()


