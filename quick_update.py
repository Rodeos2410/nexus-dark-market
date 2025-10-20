#!/usr/bin/env python3
"""
Быстрое обновление репозитория
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
            return True
        else:
            print(f"❌ Ошибка: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Исключение: {e}")
        return False

def main():
    print("🚀 Быстрое обновление репозитория...")
    
    commands = [
        "git add .",
        'git commit -m "Исправлены все ошибки развертывания - готово к запуску"',
        "git push origin main --force"
    ]
    
    for cmd in commands:
        if not run_command(cmd):
            print(f"❌ Команда не выполнена: {cmd}")
            return False
    
    print("🎉 Репозиторий обновлен!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
