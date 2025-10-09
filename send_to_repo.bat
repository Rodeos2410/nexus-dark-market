@echo off
echo 🚀 ОТПРАВКА ИЗМЕНЕНИЙ В РЕПОЗИТОРИЙ
echo ======================================

echo 📁 Добавляем все файлы...
git add .

echo 💾 Создаем коммит...
git commit -m "Add two-factor authentication system"

echo 🌐 Отправляем в репозиторий...
git push origin main

echo 🎉 ГОТОВО! Изменения отправлены в репозиторий!
pause
