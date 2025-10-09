#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Проверка готовности файлов для обновления на GitHub
"""

import os
import sys

def check_file_exists(filepath, description):
    """Проверяет существование файла"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} - НЕ НАЙДЕН")
        return False

def check_file_content(filepath, required_content, description):
    """Проверяет содержимое файла"""
    if not os.path.exists(filepath):
        print(f"❌ {description}: файл не найден")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if required_content in content:
            print(f"✅ {description}: содержимое корректно")
            return True
        else:
            print(f"⚠️ {description}: содержимое может быть неполным")
            return False
    except Exception as e:
        print(f"❌ {description}: ошибка чтения - {e}")
        return False

def main():
    """Основная функция проверки"""
    print("🔍 Проверка готовности к обновлению на GitHub")
    print("=" * 60)
    
    all_ready = True
    
    # Проверяем основные файлы
    print("\n📁 Основные файлы:")
    files_to_check = [
        ("app.py", "Основное приложение Flask"),
        ("telegram_bot.py", "Telegram бот с админ панелью"),
        ("config.py", "Конфигурация приложения"),
        ("requirements.txt", "Зависимости Python"),
        ("Procfile", "Команда запуска для Render"),
        ("render.yaml", "Конфигурация Render"),
        ("runtime.txt", "Версия Python"),
    ]
    
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_ready = False
    
    # Проверяем скрипты
    print("\n🔧 Скрипты:")
    scripts_to_check = [
        ("init_render.py", "Инициализация для Render"),
        ("setup_webhook.py", "Настройка webhook"),
        ("test_all_components.py", "Тестирование компонентов"),
        ("test_callback_buttons.py", "Тест кнопок админ панели"),
        ("test_webhook_callbacks.py", "Тест webhook с callback"),
    ]
    
    for filepath, description in scripts_to_check:
        if not check_file_exists(filepath, description):
            all_ready = False
    
    # Проверяем документацию
    print("\n📚 Документация:")
    docs_to_check = [
        ("FINAL_DEPLOYMENT_GUIDE.md", "Инструкция по деплою"),
        ("ADMIN_PANEL_BUTTONS_GUIDE.md", "Руководство по админ панели"),
        ("GITHUB_REPOSITORY_UPDATE_GUIDE.md", "Инструкция по обновлению GitHub"),
    ]
    
    for filepath, description in docs_to_check:
        if not check_file_exists(filepath, description):
            all_ready = False
    
    # Проверяем шаблоны
    print("\n🎨 Шаблоны:")
    templates_dir = "templates"
    if os.path.exists(templates_dir):
        templates = [
            "admin.html",
            "profile.html", 
            "base.html",
            "login.html",
            "register.html",
            "market.html"
        ]
        
        for template in templates:
            template_path = os.path.join(templates_dir, template)
            if not check_file_exists(template_path, f"Шаблон {template}"):
                all_ready = False
    else:
        print("❌ Папка templates не найдена")
        all_ready = False
    
    # Проверяем статические файлы
    print("\n🎨 Статические файлы:")
    static_dir = "static"
    if os.path.exists(static_dir):
        print("✅ Папка static найдена")
        
        css_dir = os.path.join(static_dir, "css")
        if os.path.exists(css_dir):
            print("✅ Папка static/css найдена")
        else:
            print("❌ Папка static/css не найдена")
            all_ready = False
    else:
        print("❌ Папка static не найдена")
        all_ready = False
    
    # Проверяем содержимое ключевых файлов
    print("\n🔍 Проверка содержимого ключевых файлов:")
    
    # Проверяем app.py на наличие callback обработки
    if not check_file_content("app.py", "callback_query", "app.py содержит обработку callback"):
        all_ready = False
    
    # Проверяем telegram_bot.py на наличие кнопок
    if not check_file_content("telegram_bot.py", "inline_keyboard", "telegram_bot.py содержит кнопки"):
        all_ready = False
    
    # Проверяем requirements.txt на наличие зависимостей
    if not check_file_content("requirements.txt", "Flask", "requirements.txt содержит Flask"):
        all_ready = False
    
    # Проверяем Procfile
    if not check_file_content("Procfile", "gunicorn app:app", "Procfile содержит правильную команду"):
        all_ready = False
    
    # Проверяем render.yaml на наличие переменных
    if not check_file_content("render.yaml", "TELEGRAM_BOT_TOKEN", "render.yaml содержит переменные Telegram"):
        all_ready = False
    
    # Итоговый результат
    print("\n" + "=" * 60)
    if all_ready:
        print("🎉 ВСЕ ФАЙЛЫ ГОТОВЫ К ОБНОВЛЕНИЮ НА GITHUB!")
        print("\n📋 Следующие шаги:")
        print("1. Запустите: python update_github_repo.py")
        print("2. Или используйте: update_github.bat")
        print("3. Или выполните команды Git вручную")
        print("\n🔗 После обновления:")
        print("- Обновите деплой на Render")
        print("- Запустите: python setup_webhook.py")
        print("- Протестируйте: python test_all_components.py")
    else:
        print("❌ НЕ ВСЕ ФАЙЛЫ ГОТОВЫ")
        print("\n💡 Исправьте ошибки и запустите проверку снова")
        print("   python check_ready_for_github.py")
    
    return all_ready

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
