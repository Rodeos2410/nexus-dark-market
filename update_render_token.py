#!/usr/bin/env python3
"""
Скрипт для обновления токена на Render
"""

import os

def main():
    """Основная функция"""
    print("🔧 Инструкция по обновлению токена на Render")
    print("=" * 50)
    
    new_token = "8458514538:AAEQruDKFmiEwRlMS-MmtUJ6D6vF2VOQ9Sc"
    
    print(f"📱 Новый токен: {new_token}")
    print()
    print("🚀 Пошаговая инструкция:")
    print()
    print("1. Зайдите в панель управления Render:")
    print("   https://dashboard.render.com/")
    print()
    print("2. Выберите ваш проект (Nexus Dark Market)")
    print()
    print("3. Перейдите в раздел 'Environment'")
    print()
    print("4. Найдите переменную TELEGRAM_BOT_TOKEN")
    print()
    print("5. Обновите значение на:")
    print(f"   {new_token}")
    print()
    print("6. Нажмите 'Save Changes'")
    print()
    print("7. Перезапустите приложение:")
    print("   - Перейдите в раздел 'Manual Deploy'")
    print("   - Нажмите 'Deploy latest commit'")
    print()
    print("8. Дождитесь завершения развертывания")
    print()
    print("✅ После этого ошибка 401 должна исчезнуть!")
    print()
    print("📊 Проверьте логи развертывания:")
    print("   - Должно появиться: '✅ Тестирование Telegram...'")
    print("   - Вместо: '❌ HTTP ошибка: 401'")
    print()
    print("🎯 Если все прошло успешно, бот будет работать!")

if __name__ == "__main__":
    main()
