#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time

def check_after_deploy():
    """Проверяет после развертывания"""
    print("🚀 ПРОВЕРКА ПОСЛЕ РАЗВЕРТЫВАНИЯ")
    print("=" * 40)
    
    base_url = "https://nexus-dark-market.onrender.com"
    
    print("⏳ Ждем 30 секунд для развертывания...")
    time.sleep(30)
    
    try:
        # Проверяем страницу админки
        response = requests.get(f"{base_url}/admin", timeout=10)
        print(f"Статус админки: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            if "Просмотр базы данных" in content:
                print("✅ Кнопка 'Просмотр базы данных' найдена!")
            else:
                print("❌ Кнопка 'Просмотр базы данных' все еще не найдена")
            
            if "/admin/database" in content:
                print("✅ Ссылка '/admin/database' найдена!")
            else:
                print("❌ Ссылка '/admin/database' все еще не найдена")
            
            if "🗄️" in content:
                print("✅ Эмодзи базы данных найдено!")
            else:
                print("❌ Эмодзи базы данных все еще не найдено")
        
        # Проверяем маршрут базы данных
        response = requests.get(f"{base_url}/admin/database", timeout=10)
        print(f"Статус базы данных: {response.status_code}")
        
        if response.status_code == 200:
            if "База данных пользователей" in response.text:
                print("✅ Маршрут базы данных работает!")
            else:
                print("⚠️ Маршрут работает, но контент неожиданный")
        elif response.status_code == 302:
            print("⚠️ Перенаправление (нужна авторизация)")
        else:
            print(f"❌ Неожиданный статус: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    check_after_deploy()
