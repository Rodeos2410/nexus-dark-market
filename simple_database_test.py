#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

def test_simple():
    """Простой тест"""
    print("🧪 ПРОСТОЙ ТЕСТ БАЗЫ ДАННЫХ")
    print("=" * 30)
    
    base_url = "https://nexus-dark-market.onrender.com"
    
    # Тестируем разные маршруты
    routes = [
        ("/", "Главная страница"),
        ("/login", "Страница входа"),
        ("/admin", "Админ панель"),
        ("/admin/database", "База данных")
    ]
    
    for route, name in routes:
        try:
            response = requests.get(f"{base_url}{route}", timeout=5)
            print(f"{name}: {response.status_code}")
        except Exception as e:
            print(f"{name}: Ошибка - {e}")

if __name__ == "__main__":
    test_simple()
