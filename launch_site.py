#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import time
import sys
import os

def launch_app():
    """Запускает Flask приложение"""
    print("🚀 Запуск Nexus Dark Market...")
    
    try:
        # Запускаем Flask приложение
        process = subprocess.Popen([
            sys.executable, 'app.py'
        ], cwd=os.path.dirname(os.path.abspath(__file__)))
        
        print(f"✅ Flask приложение запущено (PID: {process.pid})")
        print("🌐 Сайт будет доступен по адресу: http://localhost:5000")
        print("⏹️  Для остановки нажмите Ctrl+C")
        
        # Ждем завершения процесса
        process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Остановка приложения...")
        process.terminate()
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")

if __name__ == "__main__":
    launch_app()
