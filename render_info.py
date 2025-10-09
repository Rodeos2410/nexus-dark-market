#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def check_render_deployment():
    """Проверяет статус деплоя на Render"""
    
    print("🚀 Проверка деплоя на Render")
    print("=" * 50)
    
    # URL вашего приложения на Render
    app_url = "https://nexus-dark-market-1.onrender.com"
    
    # Проверяем главную страницу
    print(f"\n1️⃣ Проверка главной страницы:")
    print(f"URL: {app_url}")
    
    try:
        response = requests.get(app_url, timeout=10)
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Приложение работает")
        elif response.status_code == 404:
            print("❌ Страница не найдена - возможно проблема с роутингом")
        else:
            print(f"⚠️ Неожиданный статус: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("⏰ Таймаут - приложение может быть в режиме сна")
    except requests.exceptions.ConnectionError:
        print("❌ Ошибка подключения - приложение недоступно")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    # Проверяем webhook
    print(f"\n2️⃣ Проверка webhook:")
    webhook_url = f"{app_url}/telegram/webhook"
    print(f"URL: {webhook_url}")
    
    try:
        response = requests.post(webhook_url, json={}, timeout=10)
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Webhook доступен")
        else:
            print(f"⚠️ Webhook недоступен: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("⏰ Таймаут webhook")
    except requests.exceptions.ConnectionError:
        print("❌ Webhook недоступен")
    except Exception as e:
        print(f"❌ Ошибка webhook: {e}")
    
    # Проверяем админ панель
    print(f"\n3️⃣ Проверка админ панели:")
    admin_url = f"{app_url}/admin"
    print(f"URL: {admin_url}")
    
    try:
        response = requests.get(admin_url, timeout=10)
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Админ панель доступна")
        elif response.status_code == 302:
            print("🔄 Редирект - требуется авторизация")
        else:
            print(f"⚠️ Админ панель недоступна: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("⏰ Таймаут админ панели")
    except requests.exceptions.ConnectionError:
        print("❌ Админ панель недоступна")
    except Exception as e:
        print(f"❌ Ошибка админ панели: {e}")
    
    print(f"\n💡 Рекомендации:")
    print("1. Проверьте логи деплоя в Render Dashboard")
    print("2. Убедитесь, что все переменные окружения настроены")
    print("3. Проверьте, что база данных PostgreSQL подключена")
    print("4. Убедитесь, что все файлы загружены в репозиторий")

def main():
    """Основная функция"""
    check_render_deployment()

if __name__ == "__main__":
    main()
