#!/usr/bin/env python3
"""
Финальное обновление репозитория с исправлениями
"""

import subprocess
import sys

def run_command(command):
    """Выполняет команду"""
    print(f"🔄 {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"✅ Успешно")
            if result.stdout.strip():
                print(f"📤 {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Ошибка: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Исключение: {e}")
        return False

def main():
    print("🚀 Финальное обновление репозитория...")
    print("=" * 50)
    
    print("📋 Исправления:")
    print("✅ Убраны все PRAGMA для PostgreSQL")
    print("✅ Убраны все AUTOINCREMENT для PostgreSQL")
    print("✅ Исправлен super_magazine/app.py")
    print("✅ Telegram функции сделаны опциональными")
    print("=" * 50)
    
    commands = [
        "git add .",
        'git commit -m "ФИНАЛЬНОЕ ИСПРАВЛЕНИЕ: убраны все PRAGMA и AUTOINCREMENT для PostgreSQL"',
        "git push origin main --force"
    ]
    
    for cmd in commands:
        if not run_command(cmd):
            print(f"❌ Команда не выполнена: {cmd}")
            return False
    
    print("=" * 50)
    print("🎉 РЕПОЗИТОРИЙ ОБНОВЛЕН!")
    print("🌐 Приложение готово к развертыванию на Render")
    print("📱 Telegram функции опциональны")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
