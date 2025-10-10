#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для исправления админа и настройки 2FA
"""

from app import app, db, User
from werkzeug.security import generate_password_hash

def fix_admin():
    """Исправляет админа и настраивает 2FA"""
    
    print("🔧 Исправление админа и настройка 2FA")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Проверяем текущих админов
            admins = User.query.filter_by(is_admin=True).all()
            print(f"📋 Найдено админов: {len(admins)}")
            
            for admin in admins:
                print(f"   - {admin.username} (ID: {admin.id})")
                print(f"     Email: {admin.email}")
                print(f"     Telegram Chat ID: {admin.telegram_chat_id}")
                print(f"     Заблокирован: {admin.is_banned}")
            
            # Ищем админа Rodeos
            rodeos_admin = User.query.filter_by(username='Rodeos').first()
            
            if rodeos_admin:
                print(f"\n✅ Админ Rodeos найден (ID: {rodeos_admin.id})")
                
                # Обновляем данные админа
                rodeos_admin.is_admin = True
                rodeos_admin.is_banned = False
                rodeos_admin.telegram_chat_id = '1172834372'
                rodeos_admin.password_hash = generate_password_hash('Rodeos24102007')
                
                db.session.commit()
                print("✅ Данные админа обновлены")
                
            else:
                print("\n❌ Админ Rodeos не найден, создаем...")
                
                # Создаем нового админа
                new_admin = User(
                    username='Rodeos',
                    email='rodeos@nexus.dark',
                    password_hash=generate_password_hash('Rodeos24102007'),
                    balance=10000.0,
                    is_admin=True,
                    is_banned=False,
                    telegram_chat_id='1172834372'
                )
                
                db.session.add(new_admin)
                db.session.commit()
                print("✅ Админ Rodeos создан")
            
            # Проверяем финальное состояние
            final_admin = User.query.filter_by(username='Rodeos').first()
            if final_admin:
                print(f"\n🎯 Финальное состояние админа:")
                print(f"   Username: {final_admin.username}")
                print(f"   Email: {final_admin.email}")
                print(f"   Is Admin: {final_admin.is_admin}")
                print(f"   Is Banned: {final_admin.is_banned}")
                print(f"   Telegram Chat ID: {final_admin.telegram_chat_id}")
                print(f"   Password Hash: {'Установлен' if final_admin.password_hash else 'НЕ УСТАНОВЛЕН'}")
                
                # Проверяем пароль
                from werkzeug.security import check_password_hash
                if check_password_hash(final_admin.password_hash, 'Rodeos24102007'):
                    print("   ✅ Пароль корректный")
                else:
                    print("   ❌ Пароль некорректный")
            
            print("\n🎉 Исправление завершено!")
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            db.session.rollback()

if __name__ == "__main__":
    fix_admin()
