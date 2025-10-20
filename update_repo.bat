@echo off
echo 🚀 Обновление репозитория...

echo 🔄 Добавляем файлы...
git add .

echo 🔄 Коммитим изменения...
git commit -m "Исправлены все ошибки развертывания на Render"

echo 🔄 Отправляем в репозиторий...
git push origin main --force

echo 🎉 Готово!
pause
