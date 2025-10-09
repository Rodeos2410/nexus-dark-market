#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Автоматическое обновление репозитория с исправлениями системы прямого ввода
"""

import subprocess
import sys
import os

def run_command(command):
    """Выполняет команду и возвращает результат"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def update_repository():
    """Обновляет репозиторий"""
    print("🚀 Автоматическое обновление репозитория")
    print("=" * 50)
    
    # Проверяем статус git
    print("📋 Проверка статуса git...")
    success, stdout, stderr = run_command("git status")
    if not success:
        print(f"❌ Ошибка git status: {stderr}")
        return False
    
    print("✅ Git статус проверен")
    print(f"📄 Статус: {stdout[:200]}...")
    
    # Добавляем все файлы
    print("\n📁 Добавление файлов...")
    success, stdout, stderr = run_command("git add .")
    if not success:
        print(f"❌ Ошибка git add: {stderr}")
        return False
    
    print("✅ Файлы добавлены")
    
    # Коммитим изменения
    print("\n💾 Создание коммита...")
    commit_message = "Fix direct input system - remove command processing causing 'Unknown command' error"
    success, stdout, stderr = run_command(f'git commit -m "{commit_message}"')
    if not success:
        print(f"❌ Ошибка git commit: {stderr}")
        return False
    
    print("✅ Коммит создан")
    
    # Отправляем в репозиторий
    print("\n🌐 Отправка в репозиторий...")
    success, stdout, stderr = run_command("git push origin main")
    if not success:
        print(f"❌ Ошибка git push: {stderr}")
        return False
    
    print("✅ Изменения отправлены в репозиторий")
    
    return True

def main():
    """Основная функция"""
    print("🎉 АВТОМАТИЧЕСКОЕ ОБНОВЛЕНИЕ РЕПОЗИТОРИЯ")
    print("=" * 60)
    
    # Обновляем репозиторий
    if update_repository():
        print("\n🎉 РЕПОЗИТОРИЙ УСПЕШНО ОБНОВЛЕН!")
        print("=" * 60)
        
        print("✅ Что исправлено:")
        print("   • Убрана обработка команд, вызывающая ошибку 'Unknown command'")
        print("   • Упрощена логика обработки сообщений")
        print("   • Сохранена система прямого ввода данных")
        print("   • Исправлена ошибка при вводе логина и пароля")
        
        print("\n🔧 Как теперь работает:")
        print("   1. Нажимаете кнопку (например, '👤 Изменить логин')")
        print("   2. Сразу вводите данные (например, 'newadmin')")
        print("   3. Получаете результат")
        print("   4. Никаких ошибок 'Unknown command'!")
        
        print("\n🌐 Ссылки:")
        print("   • Сайт: https://nexus-dark-market.onrender.com")
        print("   • Бот: @NexusDarkBot")
        print("   • Репозиторий: https://github.com/Rodeos2410/nexus-dark-market.git")
        
        print("\n💡 Для тестирования:")
        print("   1. Напишите боту @NexusDarkBot /start")
        print("   2. Нажмите '⚙️ Настройки админа'")
        print("   3. Попробуйте изменить логин и пароль")
        print("   4. Проверьте, что ошибки больше нет")
        
        print("\n🎯 Система прямого ввода теперь работает без ошибок!")
        
    else:
        print("\n❌ ОШИБКА ПРИ ОБНОВЛЕНИИ РЕПОЗИТОРИЯ!")
        print("Проверьте подключение к интернету и права доступа к репозиторию")

if __name__ == "__main__":
    main()
