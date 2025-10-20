#!/usr/bin/env python3
"""
Простой скрипт для обновления репозитория
"""

import subprocess
import sys

def run_command(command):
    """Выполняет команду"""
    print(f"🔄 Выполняем: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"✅ Успешно")
            if result.stdout.strip():
                print(f"📤 Вывод: {result.stdout.strip()}")
        else:
            print(f"❌ Ошибка")
            if result.stderr.strip():
                print(f"📥 Ошибка: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Исключение: {e}")
        return False

def main():
    print("🚀 Обновление репозитория...")
    
    # Добавляем все файлы
    if not run_command("git add ."):
        return False
    
    # Коммитим
    if not run_command('git commit -m "Исправлены все ошибки развертывания на Render"'):
        return False
    
    # Принудительно отправляем
    if not run_command("git push origin main --force"):
        return False
    
    print("🎉 Репозиторий обновлен!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
