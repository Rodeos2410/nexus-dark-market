import os
import sys

# Добавляем путь к проекту в sys.path
project_path = r"C:\Users\Родион\OneDrive\Рабочий стол\диплоная"
sys.path.insert(0, project_path)

# Переходим в директорию проекта
os.chdir(project_path)

# Импортируем и запускаем приложение
from app import app

if __name__ == '__main__':
    print("Запуск Nexus Dark Market...")
    print("Приложение будет доступно по адресу: http://localhost:5000")
    print("Для остановки нажмите Ctrl+C")
    app.run(debug=True, host='0.0.0.0', port=5000)

