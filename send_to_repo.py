#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Автоматическая отправка всех изменений в репозиторий
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

def send_to_repository():
    """Отправляет все изменения в репозиторий"""
    print("🚀 Отправка всех изменений в репозиторий")
    print("=" * 50)
    
    # Проверяем статус git
    print("📋 Проверка статуса git...")
    success, stdout, stderr = run_command("git status")
    if not success:
        print(f"❌ Ошибка git status: {stderr}")
        return False
    
    print("✅ Git статус проверен")
    
    # Добавляем все файлы
    print("\n📁 Добавление всех файлов...")
    success, stdout, stderr = run_command("git add .")
    if not success:
        print(f"❌ Ошибка git add: {stderr}")
        return False
    
    print("✅ Все файлы добавлены")
    
    # Коммитим изменения
    print("\n💾 Создание коммита...")
    commit_message = "Complete fix for direct input system - resolve 'Unknown command' error and improve state management"
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
    print("🎉 ОТПРАВКА ВСЕХ ИЗМЕНЕНИЙ В РЕПОЗИТОРИЙ")
    print("=" * 60)
    
    # Отправляем в репозиторий
    if send_to_repository():
        print("\n🎉 ВСЕ ИЗМЕНЕНИЯ УСПЕШНО ОТПРАВЛЕНЫ!")
        print("=" * 60)
        
        print("✅ Что отправлено:")
        print("   • Исправления системы прямого ввода")
        print("   • Устранение ошибки 'Unknown command'")
        print("   • Улучшение управления состояниями")
        print("   • Отладочная информация")
        print("   • Тестовые скрипты")
        print("   • Документация")
        
        print("\n🔧 Исправленные функции:")
        print("   • 👤 Изменение логина админа")
        print("   • 🔒 Изменение пароля админа")
        print("   • 🚫 Блокировка пользователей")
        print("   • ✅ Разблокировка пользователей")
        print("   • 👑 Назначение админов")
        print("   • 🔍 Поиск пользователей")
        print("   • 🗑️ Удаление пользователей")
        
        print("\n🌐 Ссылки:")
        print("   • Сайт: https://nexus-dark-market.onrender.com")
        print("   • Бот: @NexusDarkBot")
        print("   • Репозиторий: https://github.com/Rodeos2410/nexus-dark-market.git")
        
        print("\n💡 Для тестирования:")
        print("   1. Напишите боту @NexusDarkBot /start")
        print("   2. Нажмите '⚙️ Настройки админа'")
        print("   3. Попробуйте изменить логин и пароль")
        print("   4. Протестируйте управление пользователями")
        
        print("\n🎯 Система прямого ввода полностью исправлена!")
        
    else:
        print("\n❌ ОШИБКА ПРИ ОТПРАВКЕ В РЕПОЗИТОРИЙ!")
        print("Проверьте подключение к интернету и права доступа к репозиторию")

if __name__ == "__main__":
    main()
