#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простая проверка базы данных
"""

from app import app, db, User, Product

def simple_check():
    """Простая проверка базы данных"""
    
    print("🔍 Простая проверка базы данных")
    print("=" * 50)
    
    with app.app_context():
        try:
            print("📋 Проверяем пользователей...")
            users = User.query.all()
            print(f"Найдено пользователей: {len(users)}")
            
            for user in users:
                print(f"  - {user.username} (ID: {user.id}, Admin: {user.is_admin})")
            
            print("\n📦 Проверяем товары...")
            products = Product.query.all()
            print(f"Найдено товаров: {len(products)}")
            
            for product in products:
                print(f"  - {product.name} (ID: {product.id}, Seller: {product.seller_id})")
            
            print("\n✅ Проверка завершена")
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    simple_check()
