Write-Host "🚀 ОТПРАВКА ИЗМЕНЕНИЙ В РЕПОЗИТОРИЙ" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green

Write-Host "📁 Добавляем все файлы..." -ForegroundColor Yellow
git add .

Write-Host "💾 Создаем коммит..." -ForegroundColor Yellow
git commit -m "Add two-factor authentication system"

Write-Host "🌐 Отправляем в репозиторий..." -ForegroundColor Yellow
git push origin main

Write-Host "🎉 ГОТОВО! Изменения отправлены в репозиторий!" -ForegroundColor Green
