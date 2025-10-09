#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт для обновления существующего репозитория на GitHub
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

def setup_git_repo():
    """Настраивает Git репозиторий"""
    print("🔧 Настройка Git репозитория")
    print("=" * 50)
    
    # Проверяем, инициализирован ли Git
    if not os.path.exists('.git'):
        print("📁 Инициализация Git репозитория...")
        if not run_command("git init", "Инициализация Git"):
            return False
    
    # Настраиваем удаленный репозиторий
    print("🔗 Настройка удаленного репозитория...")
    
    # Удаляем существующий remote (если есть)
    run_command("git remote remove origin", "Удаление старого remote")
    
    # Добавляем новый remote
    if not run_command("git remote add origin https://github.com/Rodeos2410/nexus-dark-market.git", "Добавление remote"):
        return False
    
    # Проверяем remote
    if not run_command("git remote -v", "Проверка remote"):
        return False
    
    return True

def force_update_files():
    """Принудительно обновляет все файлы"""
    print("\n📁 Принудительное обновление файлов")
    print("=" * 50)
    
    # Добавляем все файлы (включая удаленные)
    if not run_command("git add -A", "Добавление всех файлов"):
        return False
    
    # Проверяем статус
    if not run_command("git status", "Проверка статуса"):
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

def force_push():
    """Принудительно отправляет изменения"""
    print("\n🚀 Принудительная отправка в GitHub")
    print("=" * 50)
    
    # Принудительно отправляем изменения
    if not run_command("git push -f origin main", "Принудительная отправка"):
        return False
    
    return True

def main():
    """Основная функция"""
    print("🔄 Обновление существующего репозитория на GitHub")
    print("=" * 60)
    print("🎯 Цель: https://github.com/Rodeos2410/nexus-dark-market.git")
    print()
    
    # Настраиваем Git репозиторий
    if not setup_git_repo():
        print("\n❌ Ошибка настройки Git репозитория")
        return False
    
    # Принудительно обновляем файлы
    if not force_update_files():
        print("\n❌ Ошибка обновления файлов")
        return False
    
    # Создаем коммит
    if not create_commit():
        print("\n❌ Ошибка создания коммита")
        return False
    
    # Принудительно отправляем
    if not force_push():
        print("\n❌ Ошибка отправки в GitHub")
        return False
    
    print("\n🎉 РЕПОЗИТОРИЙ УСПЕШНО ОБНОВЛЕН!")
    print("=" * 60)
    
    print("\n📋 Что сделано:")
    print("✅ Git репозиторий настроен")
    print("✅ Все файлы обновлены")
    print("✅ Создан коммит с описанием")
    print("✅ Изменения отправлены в GitHub")
    
    print("\n🔗 Проверьте репозиторий:")
    print("https://github.com/Rodeos2410/nexus-dark-market")
    
    print("\n🔧 Следующие шаги:")
    print("1. Обновите деплой на Render")
    print("2. Запустите: python setup_webhook.py")
    print("3. Протестируйте: python test_all_components.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
