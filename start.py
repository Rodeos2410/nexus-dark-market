#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

def main():
    print("Запуск Nexus Dark Market...")
    print("Текущая директория:", os.getcwd())
    
    try:
        # Импортируем и запускаем приложение
        from app import app
        
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


