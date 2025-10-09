#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт для автоматизации обновления репозитория на GitHub
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Выполняет команду и выводит результат"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - успешно")
            if result.stdout:
                print(f"   {result.stdout.strip()}")
        else:
            print(f"❌ {description} - ошибка")
            if result.stderr:
                print(f"   {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - исключение: {e}")
        return False
    return True

def check_git_status():
    """Проверяет статус Git репозитория"""
    print("🔍 Проверка статуса Git репозитория")
    print("=" * 50)
    
    # Проверяем, инициализирован ли Git
    if not os.path.exists('.git'):
        print("❌ Git репозиторий не инициализирован")
        return False
    
    # Проверяем статус
    if not run_command("git status", "Проверка статуса Git"):
        return False
    
    return True

def add_files():
    """Добавляет все файлы в Git"""
    print("\n📁 Добавление файлов в Git")
    print("=" * 50)
    
    # Добавляем все файлы
    if not run_command("git add .", "Добавление всех файлов"):
        return False
    
    # Проверяем статус после добавления
    if not run_command("git status", "Проверка статуса после добавления"):
        return False
    
    return True

def create_commit():
    """Создает коммит"""
    print("\n💾 Создание коммита")
    print("=" * 50)
    
    commit_message = """Complete admin panel with buttons and Render deployment setup

- Added full admin panel with inline buttons in Telegram bot
- Fixed webhook to handle callback queries
- Updated requirements.txt with all dependencies
- Fixed Procfile for Render deployment
- Added render.yaml with environment variables
- Created initialization scripts for Render
- Added comprehensive testing scripts
- Updated app.py with callback handling
- All components ready for production deployment"""
    
    if not run_command(f'git commit -m "{commit_message}"', "Создание коммита"):
        return False
    
    return True

def push_to_github():
    """Отправляет изменения в GitHub"""
    print("\n🚀 Отправка в GitHub")
    print("=" * 50)
    
    # Проверяем, есть ли удаленный репозиторий
    result = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
    if result.returncode != 0 or not result.stdout.strip():
        print("❌ Удаленный репозиторий не настроен")
        print("💡 Настройте репозиторий командой:")
        print("   git remote add origin https://github.com/ВАШ_USERNAME/ВАШ_REPOSITORY.git")
        return False
    
    print(f"📡 Удаленный репозиторий:")
    print(f"   {result.stdout.strip()}")
    
    # Отправляем изменения
    if not run_command("git push origin main", "Отправка в GitHub"):
        print("💡 Попробуйте:")
        print("   git push -u origin main")
        return False
    
    return True

def check_key_files():
    """Проверяет наличие ключевых файлов"""
    print("\n📋 Проверка ключевых файлов")
    print("=" * 50)
    
    key_files = [
        "app.py",
        "telegram_bot.py", 
        "config.py",
        "requirements.txt",
        "Procfile",
        "render.yaml",
        "runtime.txt",
        "init_render.py",
        "setup_webhook.py",
        "test_all_components.py"
    ]
    
    missing_files = []
    for file in key_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - отсутствует")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️ Отсутствуют файлы: {', '.join(missing_files)}")
        return False
    
    return True

def main():
    """Основная функция"""
    print("🔄 Автоматическое обновление репозитория на GitHub")
    print("=" * 60)
    
    # Проверяем ключевые файлы
    if not check_key_files():
        print("\n❌ Не все ключевые файлы найдены")
        return False
    
    # Проверяем статус Git
    if not check_git_status():
        print("\n❌ Проблемы с Git репозиторием")
        return False
    
    # Добавляем файлы
    if not add_files():
        print("\n❌ Ошибка добавления файлов")
        return False
    
    # Создаем коммит
    if not create_commit():
        print("\n❌ Ошибка создания коммита")
        return False
    
    # Отправляем в GitHub
    if not push_to_github():
        print("\n❌ Ошибка отправки в GitHub")
        return False
    
    print("\n🎉 РЕПОЗИТОРИЙ УСПЕШНО ОБНОВЛЕН!")
    print("=" * 60)
    
    print("\n📋 Что сделано:")
    print("✅ Все файлы добавлены в Git")
    print("✅ Создан коммит с описанием")
    print("✅ Изменения отправлены в GitHub")
    
    print("\n🔧 Следующие шаги:")
    print("1. Зайдите на GitHub и проверьте файлы")
    print("2. Обновите деплой на Render")
    print("3. Запустите: python setup_webhook.py")
    print("4. Протестируйте: python test_all_components.py")
    
    print("\n🔗 Проверьте ваш репозиторий на GitHub!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
