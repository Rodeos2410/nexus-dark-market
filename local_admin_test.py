#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# Добавляем текущую директорию в путь для импорта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram_bot import handle_admin_command

def test_admin_panel():
    """Тестирует админ панель локально"""
    
    print("🔧 Тестирование админ панели")
    print("=" * 50)
    
    admin_chat_id = "1172834372"
    
    # Тестовые команды
    test_commands = [
        "/start",
        "/menu",
        "/stats", 
        "/users",
        "/help"
    ]
    
    for command in test_commands:
        print(f"\n📱 Команда: {command}")
        print("-" * 30)
        
        try:
            response, keyboard = handle_admin_command(command, admin_chat_id)
            
            print(f"📝 Ответ:")
            print(response)
            
            if keyboard:
                print(f"\n⌨️ Клавиатура:")
                print(json.dumps(keyboard, indent=2, ensure_ascii=False))
            else:
                print(f"\n⌨️ Клавиатура: Нет")
                
        except Exception as e:
            print(f"❌ Ошибка: {e}")
        
        print()

if __name__ == "__main__":
    import json
    test_admin_panel()
