#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт для запуска приложения с отладкой
"""

import os
import sys

def main():
    print("🚀 Запуск приложения с отладкой")
    print("=" * 40)
    
    # Проверяем, что мы в правильной директории
    if not os.path.exists("app.py"):
        print("❌ Файл app.py не найден!")
        print("💡 Убедитесь, что вы находитесь в директории проекта")
        return
    
    print("✅ Файл app.py найден")
    
    # Проверяем базу данных
    if not os.path.exists("instance/nexus_dark.db"):
        print("❌ База данных не найдена!")
        print("💡 Запустите приложение для создания базы данных")
        return
    
    print("✅ База данных найдена")
    
    # Запускаем приложение
    print("\n🔄 Запуск приложения...")
    print("💡 Следите за логами в консоли для отладки")
    print("💡 Нажмите Ctrl+C для остановки")
    
    try:
        # Импортируем и запускаем приложение
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n🛑 Приложение остановлено")
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")

if __name__ == "__main__":
    main()



