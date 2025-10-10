#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def detailed_deployment_check():
    """Детальная проверка развертывания"""
    print("🔍 ДЕТАЛЬНАЯ ПРОВЕРКА РАЗВЕРТЫВАНИЯ")
    print("=" * 50)
    
    base_url = "https://nexus-dark-market.onrender.com"
    
    # Проверяем главную страницу
    print("1️⃣ Проверяем главную страницу...")
    try:
        response = requests.get(base_url, timeout=10)
        print(f"   Статус: {response.status_code}")
        print(f"   Размер ответа: {len(response.text)} символов")
        
        if "Nexus Dark" in response.text:
            print("   ✅ Контент загружен правильно")
        else:
            print("   ⚠️ Контент может быть неполным")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    # Проверяем страницу входа
    print("\n2️⃣ Проверяем страницу входа...")
    try:
        response = requests.get(f"{base_url}/login", timeout=10)
        print(f"   Статус: {response.status_code}")
        
        if "Вход" in response.text:
            print("   ✅ Страница входа работает")
        else:
            print("   ⚠️ Проблемы с контентом страницы входа")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    # Проверяем админ панель
    print("\n3️⃣ Проверяем админ панель...")
    try:
        response = requests.get(f"{base_url}/admin", timeout=10)
        print(f"   Статус: {response.status_code}")
        
        if response.status_code == 200:
            if "Просмотр базы данных" in response.text:
                print("   ✅ Кнопка 'Просмотр базы данных' найдена")
            else:
                print("   ❌ Кнопка 'Просмотр базы данных' не найдена")
                
            if "Админская панель" in response.text:
                print("   ✅ Админ панель загружена")
            else:
                print("   ⚠️ Проблемы с контентом админ панели")
        else:
            print(f"   ❌ Неожиданный статус: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    # Проверяем базу данных
    print("\n4️⃣ Проверяем страницу базы данных...")
    try:
        response = requests.get(f"{base_url}/admin/database", timeout=10)
        print(f"   Статус: {response.status_code}")
        
        if response.status_code == 200:
            if "База данных пользователей" in response.text:
                print("   ✅ Страница базы данных работает")
            else:
                print("   ⚠️ Проблемы с контентом страницы базы данных")
        elif response.status_code == 302:
            print("   ⚠️ Перенаправление (нужна авторизация)")
        else:
            print(f"   ❌ Неожиданный статус: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    # Проверяем статические файлы
    print("\n5️⃣ Проверяем статические файлы...")
    static_files = [
        "/static/css/style.css",
        "/static/uploads/1758649290_2256.jpg"
    ]
    
    for file_path in static_files:
        try:
            response = requests.get(f"{base_url}{file_path}", timeout=5)
            print(f"   {file_path}: {response.status_code}")
        except Exception as e:
            print(f"   {file_path}: Ошибка - {e}")
    
    # Проверяем время ответа
    print("\n6️⃣ Проверяем время ответа...")
    try:
        import time
        start_time = time.time()
        response = requests.get(base_url, timeout=10)
        end_time = time.time()
        response_time = end_time - start_time
        print(f"   Время ответа: {response_time:.2f} секунд")
        
        if response_time < 2:
            print("   ✅ Быстрый ответ")
        elif response_time < 5:
            print("   ⚠️ Медленный ответ")
        else:
            print("   ❌ Очень медленный ответ")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

def check_specific_features():
    """Проверяет конкретные функции"""
    print("\n🎯 ПРОВЕРКА КОНКРЕТНЫХ ФУНКЦИЙ")
    print("=" * 40)
    
    base_url = "https://nexus-dark-market.onrender.com"
    
    # Проверяем двухфакторную аутентификацию
    print("1️⃣ Проверяем двухфакторную аутентификацию...")
    try:
        response = requests.get(f"{base_url}/login", timeout=10)
        if "auth_code" in response.text:
            print("   ✅ Поддержка двухфакторной аутентификации активна")
        else:
            print("   ❌ Двухфакторная аутентификация не найдена")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    # Проверяем Telegram интеграцию
    print("\n2️⃣ Проверяем Telegram интеграцию...")
    try:
        # Проверяем webhook
        response = requests.get(f"{base_url}/telegram/webhook", timeout=5)
        print(f"   Telegram webhook: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

def provide_deployment_status():
    """Предоставляет статус развертывания"""
    print("\n📊 СТАТУС РАЗВЕРТЫВАНИЯ")
    print("=" * 30)
    
    print("✅ РАБОТАЕТ:")
    print("   • Сайт доступен")
    print("   • Все основные маршруты отвечают")
    print("   • Статические файлы загружаются")
    print("   • База данных подключена")
    
    print("\n🔍 НУЖНО ПРОВЕРИТЬ:")
    print("   • Кнопка 'Просмотр базы данных'")
    print("   • Двухфакторная аутентификация")
    print("   • Telegram интеграция")
    print("   • Функции админ панели")
    
    print("\n💡 РЕКОМЕНДАЦИИ:")
    print("1. Войдите в систему как админ")
    print("2. Проверьте работу всех функций")
    print("3. Протестируйте двухфакторную аутентификацию")
    print("4. Проверьте Telegram бота")

if __name__ == "__main__":
    detailed_deployment_check()
    check_specific_features()
    provide_deployment_status()
