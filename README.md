# Habit Tracker Backend API

Бэкенд-часть SPA веб-приложения для управления привычками с интеграцией Telegram-бота для отправки напоминаний.

## 📋 О проекте

Приложение помогает пользователям формировать полезные привычки и отслеживать их выполнение. Пользователи могут создавать привычки, указывать время и место выполнения, получать напоминания в Telegram.

### Основные возможности

- Регистрация и аутентификация пользователей (JWT)
- Управление привычками (CRUD операции)
- Разделение привычек на полезные и приятные
- Валидация привычек по заданным правилам
- Публичные привычки для всех пользователей
- Пагинация списка привычек
- Отправка напоминаний через Telegram (Celery)
- Документация API (Swagger/ReDoc)

## 🛠 Технологии

- **Python** 3.12
- **Django** 5.1
- **Django REST Framework** 3.15
- **PostgreSQL** - база данных
- **Redis** - брокер для Celery
- **Celery** - отложенные задачи
- **Celery Beat** - периодические задачи
- **JWT** - аутентификация
- **Telegram Bot API** - отправка уведомлений
- **drf-yasg** - документация API

## 📁 Структура проекта
coursework_5/
├── coursework_5/ # Настройки проекта
│ ├── init.py
│ ├── settings.py
│ ├── urls.py
│ ├── celery.py
│ ├── wsgi.py
│ └── asgi.py
├── users/ # Приложение пользователей
│ ├── init.py
│ ├── admin.py
│ ├── apps.py
│ ├── models.py
│ ├── serializers.py
│ ├── urls.py
│ ├── views.py
│ └── tests.py
├── habits/ # Приложение привычек
│ ├── init.py
│ ├── admin.py
│ ├── apps.py
│ ├── models.py
│ ├── serializers.py
│ ├── urls.py
│ ├── views.py
│ ├── permissions.py
│ ├── validators.py
│ ├── tasks.py
│ ├── pagination.py
│ └── tests.py
├── manage.py
├── pyproject.toml
├── .env
├── .env.example
├── .flake8
├── .gitignore
└── README.md


## 🚀 Установка и запуск

### Требования

- Python 3.12+
- PostgreSQL
- Redis
- Poetry

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-username/coursework-5.git
cd coursework-5

