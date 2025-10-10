#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Финальное исправление админа
"""

from app import app, db, User, Product
from werkzeug.security import generate_password_hash

def final_admin_fix():
    """Финальное исправление админа"""
    
    print("🔧 Финальное исправление админа")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Находим админа Rodeos
            rodeos_admin = User.query.filter_by(username='Rodeos').first()
            
            if not rodeos_admin:
                print("👑 Создание админа Rodeos...")
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
                print(f"✅ Админ Rodeos найден с ID: {rodeos_admin.id}")
                # Обновляем данные
                rodeos_admin.email = 'rodeos@nexus.dark'
                rodeos_admin.password_hash = generate_password_hash('Rodeos24102007')
                rodeos_admin.is_admin = True
                rodeos_admin.is_banned = False
                rodeos_admin.telegram_chat_id = '1172834372'
                print("✅ Данные админа Rodeos обновлены")
            
            # Переназначаем товар "адм" на Rodeos
            product_adm = Product.query.filter_by(id=8).first()
            if product_adm:
                print(f"🔄 Переназначаем товар '{product_adm.name}' на Rodeos")
                product_adm.seller_id = rodeos_admin.id
                print("✅ Товар переназначен")
            
            # Удаляем старого админа admin
            old_admin = User.query.filter_by(username='admin').first()
            if old_admin:
                print(f"🗑️ Удаляем старого админа: {old_admin.username} (ID: {old_admin.id})")
                db.session.delete(old_admin)
                print("✅ Старый админ удален")
            
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
                for product in products:
                    print(f"     - {product.name} (ID: {product.id})")
                print()
            
            print("🎉 Финальное исправление завершено!")
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            db.session.rollback()
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    final_admin_fix()
