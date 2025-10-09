#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os

def run_command(command):
    """Выполняет команду"""
    try:
        print(f"Выполняю: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"✅ Успешно: {result.stdout}")
        else:
            print(f"❌ Ошибка: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Исключение: {e}")
        return False

def main():
    """Основная функция"""
    print("🚀 ОТПРАВКА ИЗМЕНЕНИЙ В РЕПОЗИТОРИЙ")
    print("=" * 50)
    
    # Проверяем статус
    print("📋 Проверяем статус git...")
    run_command("git status")
    
    # Добавляем все файлы
    print("\n📁 Добавляем все файлы...")
    if not run_command("git add ."):
        print("❌ Не удалось добавить файлы")
        return
    
    # Проверяем статус после добавления
    print("\n📋 Статус после добавления...")
    run_command("git status")
    
    # Коммитим
    print("\n💾 Создаем коммит...")
    if not run_command('git commit -m "Add two-factor authentication system"'):
        print("❌ Не удалось создать коммит")
        return
    
    # Отправляем
    print("\n🌐 Отправляем в репозиторий...")
    if not run_command("git push origin main"):
        print("❌ Не удалось отправить в репозиторий")
        return
    
    print("\n🎉 ВСЕ ИЗМЕНЕНИЯ ОТПРАВЛЕНЫ В РЕПОЗИТОРИЙ!")
    print("🔐 Система двухфакторной аутентификации развернута!")

if __name__ == "__main__":
    main()
