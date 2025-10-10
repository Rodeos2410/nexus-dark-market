#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для исправления админа с учетом товаров
"""

from app import app, db, User, Product
from werkzeug.security import generate_password_hash

def fix_admin_with_products():
    """Исправляет админа с учетом товаров"""
    
    print("🔧 Исправление админа с учетом товаров")
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
                
                # Проверяем товары админа
                products = Product.query.filter_by(seller_id=admin.id).all()
                print(f"     Товаров: {len(products)}")
            
            # Находим админа Rodeos или создаем его
            rodeos_admin = User.query.filter_by(username='Rodeos').first()
            
            if not rodeos_admin:
                print("\n👑 Создание админа Rodeos...")
                rodeos_admin = User(
                    username='Rodeos',
                    email='rodeos@nexus.dark',
                    password_hash=generate_password_hash('Rodeos24102007'),
                    balance=10000.0,
                    is_admin=True,
                    is_banned=False,
                    telegram_chat_id='1172834372'
                )
                db.session.add(rodeos_admin)
                db.session.flush()  # Получаем ID
                print(f"✅ Админ Rodeos создан с ID: {rodeos_admin.id}")
            else:
                print(f"\n✅ Админ Rodeos найден с ID: {rodeos_admin.id}")
                # Обновляем данные
                rodeos_admin.email = 'rodeos@nexus.dark'
                rodeos_admin.password_hash = generate_password_hash('Rodeos24102007')
                rodeos_admin.is_admin = True
                rodeos_admin.is_banned = False
                rodeos_admin.telegram_chat_id = '1172834372'
                print("✅ Данные админа Rodeos обновлены")
            
            # Переназначаем все товары админов на Rodeos
            for admin in admins:
                if admin.id != rodeos_admin.id:
                    products = Product.query.filter_by(seller_id=admin.id).all()
                    print(f"\n🔄 Переназначаем {len(products)} товаров от {admin.username} на Rodeos")
                    
                    for product in products:
                        product.seller_id = rodeos_admin.id
                        print(f"   - Товар '{product.name}' переназначен")
            
            # Удаляем старых админов (кроме Rodeos)
            for admin in admins:
                if admin.id != rodeos_admin.id:
                    print(f"\n🗑️ Удаляем админа: {admin.username} (ID: {admin.id})")
                    db.session.delete(admin)
            
            # Сохраняем все изменения
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
                
                # Проверяем товары
                products = Product.query.filter_by(seller_id=admin.id).all()
                print(f"   Товаров: {len(products)}")
                print()
            
            print("🎉 Исправление завершено!")
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            db.session.rollback()

if __name__ == "__main__":
    fix_admin_with_products()
