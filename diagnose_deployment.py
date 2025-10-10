#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time

def diagnose_deployment():
    """Диагностирует проблемы развертывания"""
    print("🔍 ДИАГНОСТИКА РАЗВЕРТЫВАНИЯ")
    print("=" * 40)
    
    base_url = "https://nexus-dark-market.onrender.com"
    
    # Проверяем доступность сайта
    print("1️⃣ Проверяем доступность сайта...")
    try:
        response = requests.get(base_url, timeout=10)
        print(f"   Статус: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Сайт доступен")
        elif response.status_code == 502:
            print("   ❌ Ошибка 502 - Bad Gateway (сервер не запущен)")
        elif response.status_code == 503:
            print("   ❌ Ошибка 503 - Service Unavailable")
        elif response.status_code == 504:
            print("   ❌ Ошибка 504 - Gateway Timeout")
        else:
            print(f"   ⚠️ Неожиданный статус: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("   ❌ Таймаут - сервер не отвечает")
    except requests.exceptions.ConnectionError:
        print("   ❌ Ошибка подключения - сервер недоступен")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    # Проверяем основные маршруты
    routes = [
        ("/", "Главная страница"),
        ("/login", "Страница входа"),
        ("/admin", "Админ панель"),
        ("/admin/database", "База данных")
    ]
    
    print("\n2️⃣ Проверяем основные маршруты...")
    for route, name in routes:
        try:
            response = requests.get(f"{base_url}{route}", timeout=5)
            print(f"   {name}: {response.status_code}")
        except Exception as e:
            print(f"   {name}: Ошибка - {e}")
    
    # Проверяем статические файлы
    print("\n3️⃣ Проверяем статические файлы...")
    try:
        response = requests.get(f"{base_url}/static/css/style.css", timeout=5)
        print(f"   CSS файл: {response.status_code}")
    except Exception as e:
        print(f"   CSS файл: Ошибка - {e}")
    
    print("\n📋 ВОЗМОЖНЫЕ ПРИЧИНЫ ОШИБОК РАЗВЕРТЫВАНИЯ:")
    print("1. 🗄️ Отсутствует DATABASE_URL")
    print("2. 🔧 Ошибки в коде Python")
    print("3. 📦 Проблемы с зависимостями")
    print("4. ⚙️ Неправильная конфигурация")
    print("5. 💾 Проблемы с базой данных")
    
    print("\n💡 РЕКОМЕНДАЦИИ:")
    print("1. Проверьте логи развертывания в панели Render")
    print("2. Убедитесь, что DATABASE_URL настроен")
    print("3. Проверьте, что все зависимости установлены")
    print("4. Убедитесь, что код синтаксически корректен")

def check_render_logs():
    """Проверяет логи Render"""
    print("\n📋 ИНСТРУКЦИЯ ПО ПРОВЕРКЕ ЛОГОВ RENDER:")
    print("=" * 50)
    
    print("1. Откройте https://dashboard.render.com")
    print("2. Войдите в свой аккаунт")
    print("3. Найдите сервис 'nexus-dark-market'")
    print("4. Нажмите на сервис")
    print("5. Перейдите в раздел 'Logs'")
    print("6. Найдите ошибки в логах развертывания")
    
    print("\n🔍 ЧТО ИСКАТЬ В ЛОГАХ:")
    print("- ❌ IndentationError")
    print("- ❌ ImportError")
    print("- ❌ ModuleNotFoundError")
    print("- ❌ Database connection errors")
    print("- ❌ Environment variable errors")
    print("- ❌ Build failures")

def provide_solutions():
    """Предоставляет решения проблем"""
    print("\n🔧 РЕШЕНИЯ ПРОБЛЕМ:")
    print("=" * 30)
    
    print("\n🗄️ ПРОБЛЕМА: DATABASE_URL не настроен")
    print("РЕШЕНИЕ:")
    print("1. Создайте PostgreSQL базу данных на Render")
    print("2. Скопируйте Connection String")
    print("3. Добавьте DATABASE_URL в Environment Variables")
    print("4. Перезапустите сервис")
    
    print("\n🔧 ПРОБЛЕМА: Ошибки в коде")
    print("РЕШЕНИЕ:")
    print("1. Проверьте синтаксис Python")
    print("2. Убедитесь в правильности отступов")
    print("3. Проверьте импорты")
    print("4. Исправьте ошибки и отправьте в репозиторий")
    
    print("\n📦 ПРОБЛЕМА: Зависимости не установлены")
    print("РЕШЕНИЕ:")
    print("1. Проверьте requirements.txt")
    print("2. Убедитесь, что все пакеты указаны")
    print("3. Проверьте совместимость версий")
    
    print("\n⚙️ ПРОБЛЕМА: Неправильная конфигурация")
    print("РЕШЕНИЕ:")
    print("1. Проверьте все Environment Variables")
    print("2. Убедитесь в правильности значений")
    print("3. Проверьте настройки сервиса")

if __name__ == "__main__":
    diagnose_deployment()
    check_render_logs()
    provide_solutions()
