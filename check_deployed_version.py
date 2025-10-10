#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re

def check_deployed_version():
    """Проверяет, какая версия кода развернута"""
    print("🔍 ПРОВЕРКА РАЗВЕРНУТОЙ ВЕРСИИ")
    print("=" * 40)
    
    base_url = "https://nexus-dark-market.onrender.com"
    
    # Проверяем админ панель
    print("1️⃣ Проверяем админ панель...")
    try:
        response = requests.get(f"{base_url}/admin", timeout=10)
        content = response.text
        
        # Ищем кнопку просмотра базы данных
        if "Просмотр базы данных" in content:
            print("   ✅ Кнопка 'Просмотр базы данных' найдена")
        else:
            print("   ❌ Кнопка 'Просмотр базы данных' НЕ найдена")
            
        # Ищем эмодзи базы данных
        if "🗄️" in content:
            print("   ✅ Эмодзи базы данных найдено")
        else:
            print("   ❌ Эмодзи базы данных НЕ найдено")
            
        # Ищем ссылку на базу данных
        if "/admin/database" in content:
            print("   ✅ Ссылка '/admin/database' найдена")
        else:
            print("   ❌ Ссылка '/admin/database' НЕ найдена")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    # Проверяем страницу входа
    print("\n2️⃣ Проверяем страницу входа...")
    try:
        response = requests.get(f"{base_url}/login", timeout=10)
        content = response.text
        
        # Ищем поля двухфакторной аутентификации
        if "auth_code" in content:
            print("   ✅ Поле 'auth_code' найдено")
        else:
            print("   ❌ Поле 'auth_code' НЕ найдено")
            
        if "show_code_input" in content:
            print("   ✅ Переменная 'show_code_input' найдена")
        else:
            print("   ❌ Переменная 'show_code_input' НЕ найдена")
            
        if "Подтвердить код" in content:
            print("   ✅ Кнопка 'Подтвердить код' найдена")
        else:
            print("   ❌ Кнопка 'Подтвердить код' НЕ найдена")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    # Проверяем страницу базы данных
    print("\n3️⃣ Проверяем страницу базы данных...")
    try:
        response = requests.get(f"{base_url}/admin/database", timeout=10)
        content = response.text
        
        if "База данных пользователей" in content:
            print("   ✅ Заголовок 'База данных пользователей' найден")
        else:
            print("   ❌ Заголовок 'База данных пользователей' НЕ найден")
            
        if "base.html" in content:
            print("   ✅ Наследование от base.html найдено")
        else:
            print("   ❌ Наследование от base.html НЕ найдено")
            
        # Проверяем, это старый HTML или новый шаблон
        if "<!DOCTYPE html>" in content and "base.html" not in content:
            print("   ⚠️ Используется старый HTML (не шаблон)")
        elif "{% extends" in content:
            print("   ✅ Используется новый шаблон")
        else:
            print("   ⚠️ Неопределенный формат")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

def check_git_status():
    """Проверяет статус git"""
    print("\n📋 СТАТУС GIT")
    print("=" * 20)
    
    import subprocess
    
    try:
        # Проверяем статус
        result = subprocess.run(["git", "status", "--porcelain"], 
                              capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            if result.stdout.strip():
                print("   ⚠️ Есть несохраненные изменения:")
                print(f"   {result.stdout.strip()}")
            else:
                print("   ✅ Все изменения сохранены")
        else:
            print(f"   ❌ Ошибка git status: {result.stderr}")
            
        # Проверяем последний коммит
        result = subprocess.run(["git", "log", "-1", "--oneline"], 
                              capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"   📝 Последний коммит: {result.stdout.strip()}")
        else:
            print(f"   ❌ Ошибка git log: {result.stderr}")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

def provide_solutions():
    """Предоставляет решения"""
    print("\n🔧 РЕШЕНИЯ ПРОБЛЕМ")
    print("=" * 30)
    
    print("\n❌ ПРОБЛЕМА: Изменения не развернулись")
    print("ВОЗМОЖНЫЕ ПРИЧИНЫ:")
    print("1. Render использует кэшированную версию")
    print("2. Изменения не были отправлены в репозиторий")
    print("3. Render не обновил код")
    print("4. Проблемы с автодеплоем")
    
    print("\n✅ РЕШЕНИЯ:")
    print("1. Принудительное обновление на Render:")
    print("   - Manual Deploy → Deploy latest commit")
    print("2. Проверка репозитория:")
    print("   - Убедитесь, что изменения в GitHub")
    print("3. Очистка кэша:")
    print("   - Restart service на Render")
    print("4. Проверка автодеплоя:")
    print("   - Убедитесь, что autoDeploy включен")

if __name__ == "__main__":
    check_deployed_version()
    check_git_status()
    provide_solutions()
