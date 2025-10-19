#!/usr/bin/env python3
"""
Скрипт для отправки исправления токена в репозиторий
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Выполняет команду и выводит результат"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"✅ {description} - успешно")
            if result.stdout.strip():
                print(f"📤 Вывод: {result.stdout.strip()}")
        else:
            print(f"❌ {description} - ошибка")
            if result.stderr.strip():
                print(f"📥 Ошибка: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - исключение: {e}")
        return False
    return True

def main():
    """Основная функция"""
    print("🚀 Отправка исправления токена в репозиторий...")
    
    # Проверяем, что мы в git репозитории
    if not os.path.exists('.git'):
        print("❌ Это не git репозиторий!")
        return False
    
    # Добавляем все файлы
    if not run_command("git add .", "Добавление файлов"):
        return False
    
    # Проверяем статус
    if not run_command("git status", "Проверка статуса"):
        return False
    
    # Коммитим изменения
    commit_message = "Исправлен токен Telegram бота - устранена ошибка 401"
    if not run_command(f'git commit -m "{commit_message}"', "Создание коммита"):
        return False
    
    # Отправляем в репозиторий
    if not run_command("git push origin main", "Отправка в репозиторий"):
        return False
    
    print("\n🎉 Исправление токена успешно отправлено в репозиторий!")
    print("\n📝 Следующие шаги:")
    print("1. Обновите переменную TELEGRAM_BOT_TOKEN на Render")
    print("2. Перезапустите приложение на Render")
    print("3. Проверьте, что ошибка 401 исчезла")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
