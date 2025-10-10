#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для очистки админов и создания правильного
"""

from app import app, db, User
from werkzeug.security import generate_password_hash

def cleanup_admins():
    """Очищает админов и создает правильного"""
    
    print("🧹 Очистка админов и создание правильного")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Удаляем всех админов
            admins = User.query.filter_by(is_admin=True).all()
            print(f"📋 Найдено админов для удаления: {len(admins)}")
            
            for admin in admins:
                print(f"   - Удаляем: {admin.username} (ID: {admin.id})")
                db.session.delete(admin)
            
            db.session.commit()
            print("✅ Все старые админы удалены")
            
            # Создаем нового правильного админа
            print("\n👑 Создание нового админа...")
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
            print("✅ Новый админ создан")
            
            # Проверяем результат
            final_admin = User.query.filter_by(is_admin=True).first()
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
            
            print("\n🎉 Очистка и создание завершены!")
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            db.session.rollback()

if __name__ == "__main__":
    cleanup_admins()
