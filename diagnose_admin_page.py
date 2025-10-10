#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re

def diagnose_admin_page():
    """Диагностирует страницу админки"""
    print("🔍 ДИАГНОСТИКА СТРАНИЦЫ АДМИНКИ")
    print("=" * 40)
    
    base_url = "https://nexus-dark-market.onrender.com"
    
    try:
        # Получаем страницу админки
        response = requests.get(f"{base_url}/admin", timeout=10)
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # Проверяем наличие кнопки
            if "Просмотр базы данных" in content:
                print("✅ Кнопка 'Просмотр базы данных' найдена в HTML")
            else:
                print("❌ Кнопка 'Просмотр базы данных' НЕ найдена в HTML")
            
            # Проверяем ссылку
            if "/admin/database" in content:
                print("✅ Ссылка '/admin/database' найдена в HTML")
            else:
                print("❌ Ссылка '/admin/database' НЕ найдена в HTML")
            
            # Проверяем наличие кнопки с эмодзи
            if "🗄️" in content:
                print("✅ Эмодзи базы данных найдено")
            else:
                print("❌ Эмодзи базы данных НЕ найдено")
            
            # Ищем все ссылки на /admin/database
            database_links = re.findall(r'href=["\']([^"\']*admin/database[^"\']*)["\']', content)
            if database_links:
                print(f"✅ Найдены ссылки на базу данных: {database_links}")
            else:
                print("❌ Ссылки на базу данных не найдены")
            
            # Проверяем, есть ли JavaScript ошибки
            if "error" in content.lower() or "ошибка" in content.lower():
                print("⚠️ Возможные ошибки в контенте")
            
            # Проверяем структуру HTML
            if "<a href=" in content and "admin/database" in content:
                print("✅ HTML структура выглядит правильно")
            else:
                print("❌ Проблемы с HTML структурой")
                
        else:
            print(f"❌ Страница недоступна: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def test_database_route_directly():
    """Тестирует маршрут базы данных напрямую"""
    print("\n🗄️ ТЕСТ МАРШРУТА БАЗЫ ДАННЫХ")
    print("=" * 40)
    
    base_url = "https://nexus-dark-market.onrender.com"
    
    try:
        response = requests.get(f"{base_url}/admin/database", timeout=10)
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            if "База данных пользователей" in content:
                print("✅ Страница базы данных загружена правильно")
            else:
                print("❌ Страница загружена, но контент неожиданный")
                print(f"Первые 200 символов: {content[:200]}")
        elif response.status_code == 302:
            print("⚠️ Перенаправление (возможно, нужна авторизация)")
        elif response.status_code == 403:
            print("⚠️ Доступ запрещен (возможно, нужны права админа)")
        else:
            print(f"❌ Неожиданный статус: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    diagnose_admin_page()
    test_database_route_directly()
