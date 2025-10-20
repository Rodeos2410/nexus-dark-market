#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Универсальный скрипт для обновления репозитория
Поддерживает Windows, Linux и macOS
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

def get_commit_message():
    """Получить сообщение коммита"""
    return "Оптимизирована админ панель и база данных для мобильных устройств"

def main():
    print("🚀 Универсальный скрипт обновления репозитория")
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
    commit_message = get_commit_message()
    if not run_command(f'git commit -m "{commit_message}"', "Создание коммита"):
        return
    
    # Получаем изменения с сервера
    if not run_command("git pull origin main", "Получение изменений с сервера"):
        return
    
    # Отправляем изменения на сервер
    if not run_command("git push origin main", "Отправка изменений на сервер"):
        return
    
    print("\n🎉 Обновление завершено успешно!")
    print("📱 Админ панель и база данных теперь оптимизированы для мобильных устройств")
    print("\n📋 Что было сделано:")
    print("   • Добавлены мобильные карточки для пользователей")
    print("   • Оптимизированы таблицы для мобильных экранов")
    print("   • Улучшена статистика с адаптивным дизайном")
    print("   • Добавлены responsive стили")
    print("   • Создан адаптивный интерфейс для всех размеров экранов")
    print("\n🌐 Теперь ваше приложение готово к развертыванию на Render!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Обновление прервано пользователем")
    except Exception as e:
        print(f"\n❌ Неожиданная ошибка: {e}")
        sys.exit(1)
