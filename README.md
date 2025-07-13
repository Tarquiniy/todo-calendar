# 📅 ToDo Calendar Planner

Планировщик дел с календарём и заметками на Django.

## 🔷 Функционал
✅ Просмотр задач на текущий день  
✅ Добавление новых задач с указанием даты и описания  
✅ База данных (PostgreSQL)  
✅ Удобная админка для управления записями

## 🔷 Технологии
- Python 3.12
- Django 5.x
- PostgreSQL
- Docker, Docker Compose
- HTML, CSS (базовый)

## 🔷 Установка

### 🚀 Запуск без Docker
```bash
git clone https://github.com/Tarquiniy/todo-calendar.git
cd todo-calendar
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
