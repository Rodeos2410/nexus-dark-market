#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Автоматическое обновление репозитория с финальной кнопочной админ панелью
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
    print("🚀 Обновление репозитория с финальной кнопочной админ панелью")
    print("=" * 70)
    
    # Проверяем статус git
    print("📋 Проверка статуса git...")
    success, stdout, stderr = run_command("git status")
    if not success:
        print(f"❌ Ошибка git status: {stderr}")
        return False
    
    print("✅ Git статус проверен")
    
    # Добавляем все файлы
    print("\n📁 Добавление файлов...")
    success, stdout, stderr = run_command("git add .")
    if not success:
        print(f"❌ Ошибка git add: {stderr}")
        return False
    
    print("✅ Файлы добавлены")
    
    # Коммитим изменения
    print("\n💾 Создание коммита...")
    commit_message = "Final button-only admin panel - remove all commands, only buttons with auto-generation"
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
    print("🎉 ФИНАЛЬНОЕ ОБНОВЛЕНИЕ РЕПОЗИТОРИЯ")
    print("=" * 50)
    
    # Обновляем репозиторий
    if update_repository():
        print("\n🎉 РЕПОЗИТОРИЙ УСПЕШНО ОБНОВЛЕН!")
        print("=" * 50)
        
        print("✅ Что обновлено:")
        print("   • Убраны все команды из админ панели")
        print("   • Оставлены только кнопки")
        print("   • Автоматическая генерация логинов и паролей")
        print("   • Упрощенная навигация")
        
        print("\n🔧 Функции админ панели:")
        print("   • 👤 Изменить логин (автоматически)")
        print("   • 🔒 Изменить пароль (автоматически)")
        print("   • ℹ️ Информация об админе")
        print("   • 📊 Статистика")
        print("   • 👥 Пользователи")
        print("   • 🔧 Управление")
        print("   • 📱 Telegram")
        
        print("\n🌐 Ссылки:")
        print("   • Сайт: https://nexus-dark-market.onrender.com")
        print("   • Бот: @NexusDarkBot")
        print("   • Репозиторий: https://github.com/Rodeos2410/nexus-dark-market.git")
        
        print("\n💡 Для тестирования:")
        print("   1. Напишите боту @NexusDarkBot /start")
        print("   2. Нажмите '⚙️ Настройки админа'")
        print("   3. Попробуйте изменить логин и пароль")
        print("   4. Проверьте вход на сайт с новыми данными")
        
        print("\n🎯 Админ панель теперь работает ТОЛЬКО с кнопками!")
        
    else:
        print("\n❌ ОШИБКА ПРИ ОБНОВЛЕНИИ РЕПОЗИТОРИЯ!")
        print("Проверьте подключение к интернету и права доступа к репозиторию")

if __name__ == "__main__":
    main()
