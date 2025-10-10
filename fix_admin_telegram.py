#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для исправления Telegram настроек админа
"""

from app import app, db, User
from werkzeug.security import generate_password_hash

def fix_admin_telegram():
    """Исправляет Telegram настройки админа"""
    
    print("🔧 Исправление Telegram настроек админа")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Проверяем всех админов
            admins = User.query.filter_by(is_admin=True).all()
            print(f"📋 Найдено админов: {len(admins)}")
            
            for admin in admins:
                print(f"   - {admin.username} (ID: {admin.id})")
                print(f"     Email: {admin.email}")
                print(f"     Telegram Chat ID: {admin.telegram_chat_id}")
                print(f"     Заблокирован: {admin.is_banned}")
            
            # Исправляем всех админов
            for admin in admins:
                print(f"\n🔧 Исправляем админа: {admin.username}")
                
                # Устанавливаем правильный Telegram Chat ID
                admin.telegram_chat_id = '1172834372'
                admin.is_admin = True
                admin.is_banned = False
                
                # Если это не Rodeos, обновляем данные
                if admin.username != 'Rodeos':
                    admin.username = 'Rodeos'
                    admin.email = 'rodeos@nexus.dark'
                    admin.password_hash = generate_password_hash('Rodeos24102007')
                
                print(f"   ✅ Telegram Chat ID установлен: {admin.telegram_chat_id}")
                print(f"   ✅ Статус админа: {admin.is_admin}")
                print(f"   ✅ Заблокирован: {admin.is_banned}")
            
            # Сохраняем изменения
            db.session.commit()
            print("\n✅ Все изменения сохранены")
            
            # Проверяем финальное состояние
            print("\n🎯 Финальное состояние админов:")
            final_admins = User.query.filter_by(is_admin=True).all()
            
            for admin in final_admins:
                print(f"   Username: {admin.username}")
                print(f"   Email: {admin.email}")
                print(f"   Is Admin: {admin.is_admin}")
                print(f"   Is Banned: {admin.is_banned}")
                print(f"   Telegram Chat ID: {admin.telegram_chat_id}")
                print(f"   Password Hash: {'Установлен' if admin.password_hash else 'НЕ УСТАНОВЛЕН'}")
                
                # Проверяем пароль
                from werkzeug.security import check_password_hash
                if check_password_hash(admin.password_hash, 'Rodeos24102007'):
                    print("   ✅ Пароль корректный")
                else:
                    print("   ❌ Пароль некорректный")
                print()
            
            print("🎉 Исправление завершено!")
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            db.session.rollback()

if __name__ == "__main__":
    fix_admin_telegram()
