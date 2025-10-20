#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для исправления живого чата
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
    print("🔧 Исправление живого чата")
    print("=" * 40)
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
    commit_message = "Исправлен живой чат: добавлена отладка и исправлена логика отображения сообщений"
    if not run_command(f'git commit -m "{commit_message}"', "Создание коммита"):
        return
    
    # Получаем изменения с сервера
    if not run_command("git pull origin main", "Получение изменений с сервера"):
        return
    
    # Отправляем изменения на сервер
    if not run_command("git push origin main", "Отправка изменений на сервер"):
        return
    
    print("\n🎉 Исправления применены успешно!")
    print("💬 Живой чат теперь должен правильно отображать сообщения")
    print("\n📋 Что было исправлено:")
    print("   • Исправлена логика определения отправителя сообщений")
    print("   • Добавлена отладочная информация в консоль браузера")
    print("   • Исправлено отображение имени отправителя")
    print("   • Улучшена обработка новых сообщений")
    print("\n🔍 Для отладки:")
    print("   1. Откройте чат в браузере")
    print("   2. Нажмите F12 для открытия DevTools")
    print("   3. Перейдите на вкладку Console")
    print("   4. Отправьте сообщение и посмотрите логи")
    print("\n🌐 Теперь чат должен работать как настоящий мессенджер!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Исправление прервано пользователем")
    except Exception as e:
        print(f"\n❌ Неожиданная ошибка: {e}")
        sys.exit(1)
