# 📅 Todo Calendar Planner

> Приложение для планирования задач с календарём, фильтрацией и CRUD.

## 🚀 Возможности
✅ Добавление/редактирование/удаление задач  
✅ Фильтрация по статусу, дате и категории  
✅ Календарь с задачами  
✅ Повторяющиеся задачи  
✅ Красивый Bootstrap интерфейс  
✅ CRUD категорий

## 🧰 Технологии
- Python 3.12
- Django 5.x
- PostgreSQL
- Docker Compose
- Bootstrap 5
- FullCalendar.js

## 🔷 Установка

### 🐳 Docker
```bash
docker-compose up --build
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
