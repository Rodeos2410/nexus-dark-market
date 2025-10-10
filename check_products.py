#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для проверки товаров
"""

from app import app, db, User, Product

def check_products():
    """Проверяет все товары"""
    
    print("📦 Проверка товаров")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Проверяем все товары
            products = Product.query.all()
            print(f"📋 Найдено товаров: {len(products)}")
            
            for product in products:
                print(f"   - ID: {product.id}")
                print(f"     Название: {product.name}")
                print(f"     Seller ID: {product.seller_id}")
                
                # Проверяем, существует ли продавец
                seller = User.query.get(product.seller_id)
                if seller:
                    print(f"     Продавец: {seller.username} (ID: {seller.id})")
                else:
                    print(f"     ❌ Продавец не найден!")
            
            # Проверяем всех пользователей
            users = User.query.all()
            print(f"\n👥 Найдено пользователей: {len(users)}")
            
            for user in users:
                print(f"   - ID: {user.id}")
                print(f"     Username: {user.username}")
                print(f"     Email: {user.email}")
                print(f"     Is Admin: {user.is_admin}")
                print(f"     Telegram Chat ID: {user.telegram_chat_id}")
                
                # Проверяем товары пользователя
                user_products = Product.query.filter_by(seller_id=user.id).all()
                print(f"     Товаров: {len(user_products)}")
                print()
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    check_products()
