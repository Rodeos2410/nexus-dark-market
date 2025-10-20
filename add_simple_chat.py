#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для добавления простого чата для тестирования
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """Выполнить команду и показать результат"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"✅ {description} - успешно")
            if result.stdout.strip():
                print(f"   Вывод: {result.stdout.strip()}")
        else:
            print(f"❌ {description} - ошибка")
            if result.stderr.strip():
                print(f"   Ошибка: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - исключение: {e}")
        return False
    return True

def main():
    print("🧪 Добавление простого чата для тестирования")
    print("=" * 50)
    print(f"🖥️  Операционная система: {platform.system()} {platform.release()}")
    print(f"🐍 Python версия: {sys.version.split()[0]}")
    print()
    
    # Проверяем, что мы в git репозитории
    if not os.path.exists('.git'):
        print("❌ Не найден .git каталог. Убедитесь, что вы в корне git репозитория.")
        return
    
    # Проверяем статус git
    print("📋 Проверка статуса репозитория...")
    status_result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if status_result.returncode == 0:
        if status_result.stdout.strip():
            print("📝 Найдены изменения для коммита:")
            print(status_result.stdout.strip())
        else:
            print("ℹ️  Нет изменений для коммита")
    
    # Добавляем все файлы
    if not run_command("git add .", "Добавление файлов"):
        return
    
    # Коммитим изменения
    commit_message = "Добавлен простой чат для тестирования отображения сообщений"
    if not run_command(f'git commit -m "{commit_message}"', "Создание коммита"):
        return
    
    # Получаем изменения с сервера
    if not run_command("git pull origin main", "Получение изменений с сервера"):
        return
    
    # Отправляем изменения на сервер
    if not run_command("git push origin main", "Отправка изменений на сервер"):
        return
    
    print("\n🎉 Простой чат добавлен успешно!")
    print("🧪 Теперь можно тестировать отображение сообщений")
    print("\n📋 Что было добавлено:")
    print("   • Простой чат без сложной логики")
    print("   • Маршрут /chat_simple/<product_id>")
    print("   • Тестовые функции для добавления сообщений")
    print("   • Автоматическое тестовое сообщение через 3 секунды")
    print("   • Кнопки для тестирования")
    print("\n🔍 Как использовать:")
    print("   1. Откройте простой чат: /chat_simple/<product_id>")
    print("   2. Нажмите F12 для открытия DevTools")
    print("   3. Перейдите на вкладку Console")
    print("   4. Посмотрите логи инициализации")
    print("   5. Используйте кнопки для тестирования:")
    print("      - 'Добавить тестовое сообщение'")
    print("      - 'Очистить чат'")
    print("   6. Или используйте функции в консоли:")
    print("      - addTestMessage()")
    print("      - clearMessages()")
    print("\n🌐 Если простой чат работает, значит проблема в сложной логике!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Добавление простого чата прервано пользователем")
    except Exception as e:
        print(f"\n❌ Неожиданная ошибка: {e}")
        sys.exit(1)
