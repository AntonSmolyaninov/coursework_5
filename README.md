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

# 📁 Структура проекта

📦 coursework_5
 ┣ 📂 config
 ┃ ┣ 📜 __init__.py
 ┃ ┣ 📜 settings.py
 ┃ ┣ 📜 urls.py
 ┃ ┗ 📜 celery.py
 ┣ 📂 habits
 ┃ ┣ 📂 migrations
 ┃ ┣ 📜 __init__.py
 ┃ ┣ 📜 models.py
 ┃ ┣ 📜 views.py
 ┃ ┣ 📜 serializers.py
 ┃ ┣ 📜 tasks.py
 ┃ ┗ 📜 tests.py
 ┣ 📂 users
 ┃ ┣ 📂 migrations
 ┃ ┣ 📜 __init__.py
 ┃ ┣ 📜 models.py
 ┃ ┣ 📜 views.py
 ┃ ┗ 📜 tests.py
 ┣ 📜 manage.py
 ┣ 📜 pyproject.toml
 ┗ 📜 README.md


## 🚀 Установка и запуск

### Требования

- **Docker Desktop** (Windows/Mac) или Docker Engine (Linux)
- **Docker Compose** v2+
- Git
- (опционально) Python 3.12+ для локальной разработки

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-username/coursework-5.git
cd coursework-5
2. Настройка переменных окружения
bash
cp .env.example .env
Отредактируйте .env файл, указав свои значения:

env
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-server-ip

DB_NAME=coursework5_db
DB_USER=postgres
DB_PASSWORD=your-strong-password
DB_HOST=db
DB_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379

TELEGRAM_BOT_TOKEN=your_telegram_bot_token
3. Запуск через Docker Compose (рекомендуется)
bash
# Собрать и запустить все контейнеры
docker compose up -d --build

# Применить миграции
docker compose exec web python manage.py migrate

# Создать суперпользователя
docker compose exec web python manage.py createsuperuser

# Собрать статические файлы
docker compose exec web python manage.py collectstatic --noinput
4. Запуск без Docker (для разработки)
bash
# Установка зависимостей через Poetry
poetry install

# Активация виртуального окружения
poetry shell

# Настройка базы данных PostgreSQL
# Создайте базу данных и настройте .env файл

# Применение миграций
python manage.py migrate

# Запуск Redis (в отдельном терминале)
redis-server

# Запуск Celery worker (в отдельном терминале)
celery -A config worker -l INFO

# Запуск Celery beat (в отдельном терминале)
celery -A config beat -l INFO

# Запуск сервера разработки
python manage.py runserver
5. Проверка работоспособности
bash
# Проверка статуса контейнеров
docker compose ps

# Проверка health endpoint
curl http://localhost:8000/health/

# Просмотр логов
docker compose logs -f
6. Остановка
bash
# Остановка всех контейнеров
docker compose down

# Остановка с удалением volumes
docker compose down -v

##CI/CD Pipeline
GitHub Actions
Проект настроен с использованием GitHub Actions для автоматического:

Запуска тестов - при каждом push в ветки main, master, develop

Проверки линтеров - Flake8, Black, isort

Сборки Docker образа - проверка возможности сборки

Автоматического деплоя - на удаленный сервер при пуше в main

Необходимые Secrets для GitHub Actions
Secret	Описание
SERVER_HOST	IP-адрес сервера
SERVER_USER	Имя пользователя на сервере
SSH_PRIVATE_KEY	Приватный SSH ключ для доступа

##Тестирование
Запуск тестов локально
bash
# Через Docker
docker compose exec web pytest

# С покрытием
docker compose exec web pytest --cov=habits --cov=users --cov-report=term

# Без Docker
poetry run pytest --cov=. --cov-fail-under=80
Запуск тестов в CI
Тесты автоматически запускаются в GitHub Actions при каждом push.

📝 Команды для управления
bash
# Просмотр логов всех сервисов
docker compose logs -f

# Просмотр логов конкретного сервиса
docker compose logs web -f
docker compose logs celery_worker -f

# Перезапуск сервиса
docker compose restart web

# Выполнение команд в контейнере
docker compose exec web python manage.py shell
docker compose exec web python manage.py dbshell

# Очистка Docker
docker system prune -a -f

##Установка на сервер
Подготовка сервера
bash
# Установка Docker
sudo apt update
sudo apt install -y docker.io docker-compose-plugin

# Добавление пользователя в группу docker
sudo usermod -aG docker $USER
newgrp docker
Настройка SSH ключа для деплоя
bash
# На сервере добавьте публичный ключ
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "ssh-rsa AAA..." >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
Ручной деплой
bash
# На сервере
git clone https://github.com/your-username/coursework-5.git
cd coursework-5
cp .env.example .env
# Отредактируйте .env
docker compose up -d --build
