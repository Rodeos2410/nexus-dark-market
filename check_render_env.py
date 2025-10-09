#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Проверка переменных окружения для Render
"""

import os

def check_environment_variables():
    """Проверяет переменные окружения"""
    print("🔧 Проверка переменных окружения для Render")
    print("=" * 60)
    
    required_vars = {
        'FLASK_ENV': 'production',
        'SECRET_KEY': 'любое значение',
        'DATABASE_URL': 'postgresql://...',
        'TELEGRAM_BOT_TOKEN': '8458514538:AAFIAT7BrKelIHie9-JscBnOlAFd_V2qyMY',
        'TELEGRAM_CHAT_ID': '1172834372'
    }
    
    print("📋 Требуемые переменные окружения:")
    print()
    
    all_set = True
    
    for var_name, expected_value in required_vars.items():
        value = os.environ.get(var_name)
        
        if value:
            # Скрываем чувствительные данные
            if 'TOKEN' in var_name or 'KEY' in var_name or 'URL' in var_name:
                display_value = f"{'*' * 10}...{value[-4:]}" if len(value) > 14 else "*" * 10
            else:
                display_value = value
            
            print(f"✅ {var_name}: {display_value}")
        else:
            print(f"❌ {var_name}: НЕ НАЙДЕНА")
            all_set = False
    
    print()
    
    if all_set:
        print("🎉 ВСЕ ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ НАСТРОЕНЫ!")
    else:
        print("⚠️ НЕКОТОРЫЕ ПЕРЕМЕННЫЕ ОТСУТСТВУЮТ")
    
    return all_set

def show_render_setup_instructions():
    """Показывает инструкции по настройке Render"""
    print("\n📚 ИНСТРУКЦИИ ПО НАСТРОЙКЕ RENDER")
    print("=" * 60)
    
    print("\n🔧 1. Создайте Web Service:")
    print("   - Зайдите в https://dashboard.render.com")
    print("   - Нажмите 'New' → 'Web Service'")
    print("   - Подключите репозиторий: Rodeos2410/nexus-dark-market")
    print("   - Branch: main")
    
    print("\n⚙️ 2. Настройте параметры:")
    print("   - Name: nexus-dark-market")
    print("   - Environment: Python 3")
    print("   - Build Command: pip install -r requirements.txt && python init_render.py")
    print("   - Start Command: gunicorn app:app")
    
    print("\n🗄️ 3. Создайте PostgreSQL Database:")
    print("   - Нажмите 'New' → 'PostgreSQL'")
    print("   - Name: nexus-dark-db")
    print("   - Plan: Free")
    
    print("\n🔑 4. Настройте переменные окружения:")
    print("   - FLASK_ENV = production")
    print("   - SECRET_KEY = (автогенерируется)")
    print("   - DATABASE_URL = (из PostgreSQL)")
    print("   - TELEGRAM_BOT_TOKEN = 8458514538:AAFIAT7BrKelIHie9-JscBnOlAFd_V2qyMY")
    print("   - TELEGRAM_CHAT_ID = 1172834372")
    
    print("\n🚀 5. Запустите деплой:")
    print("   - Нажмите 'Manual Deploy' → 'Deploy latest commit'")
    print("   - Дождитесь завершения (5-10 минут)")
    
    print("\n🔗 6. Настройте webhook:")
    print("   - Запустите: python setup_webhook.py")
    print("   - Или используйте: python setup_render_automatically.py")

def main():
    """Основная функция"""
    print("🚀 Настройка Render для Nexus Dark Market")
    print("=" * 70)
    
    # Проверяем переменные окружения
    env_ok = check_environment_variables()
    
    # Показываем инструкции
    show_render_setup_instructions()
    
    print("\n📋 СЛЕДУЮЩИЕ ШАГИ:")
    print("=" * 60)
    
    if env_ok:
        print("✅ Переменные окружения настроены")
        print("🚀 Запустите: python setup_render_automatically.py")
    else:
        print("⚠️ Настройте переменные окружения в Render Dashboard")
        print("📚 Следуйте инструкциям выше")
    
    print("\n🔗 Полезные ссылки:")
    print("   - Render Dashboard: https://dashboard.render.com")
    print("   - Репозиторий: https://github.com/Rodeos2410/nexus-dark-market")
    print("   - Telegram бот: @NexusDarkBot")
    
    return env_ok

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
