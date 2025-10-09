#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

def main():
    # Путь к проекту
    project_dir = r"C:\Users\Родион\OneDrive\Рабочий стол\диплоная"
    
    # Проверяем существование директории
    if not os.path.exists(project_dir):
        print(f"Ошибка: Директория {project_dir} не найдена!")
        return 1
    
    # Переходим в директорию проекта
    os.chdir(project_dir)
    print(f"Перешли в директорию: {os.getcwd()}")
    
    # Проверяем существование app.py
    app_file = os.path.join(project_dir, "app.py")
    if not os.path.exists(app_file):
        print(f"Ошибка: Файл {app_file} не найден!")
        return 1
    
    # Добавляем путь к проекту в sys.path
    sys.path.insert(0, project_dir)
    
    try:
        # Импортируем и запускаем приложение
        print("Импортируем приложение...")
        from app import app
        
        print("Запуск Nexus Dark Market...")
        print("Приложение будет доступно по адресу: http://localhost:5000")
        print("Для остановки нажмите Ctrl+C")
        
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except Exception as e:
        print(f"Ошибка при запуске приложения: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())


