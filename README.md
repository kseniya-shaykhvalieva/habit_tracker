# Трекер привычек

Веб-приложение на Django для отслеживания полезных привычек с интеграцией Telegram-уведомлений.

## Основной функционал

- Создание, просмотр, редактирование и удаление привычек.
- Разграничение прав: пользователь видит и управляет только своими привычками.
- Публичные привычки доступны для просмотра всем пользователям.
- Пагинация (5 привычек на страницу).
- Валидация данных при создании привычек.
- Авторизация через JWT.
- Документация API (drf-spectacular).
- Фоновые задачи Celery:
  - Отправка уведомлений в Telegram о привычках.
- CORS настроен для взаимодействия с фронтендом.

## Структура проекта
``` 
habit_tracker/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── habits/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── paginations.py
│   ├── serializers.py
│   ├── tasks.py
│   ├── tests.py
│   ├── urls.py
│   ├── validations.py
│   └── views.py
├── users/
│   ├── management/commands/
│   │   ├── __init__.py
│   │   └── csu.py
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── htmlcov/
├── .coverage
├── .env
├── .env_template
├── .flake8
├── .gitignore
├── celerybeat-schedule
├── manage.py
├── poetry.lock
├── pyproject.toml
└── README.md
```

## Установка и запуск

1. **Клонирование и переход в директорию**

2. **Установка зависимостей (Poetry):**
``` 
poetry install
```

3. **Настройка переменных окружения:**
- Скопируйте `.env.sample` в `.env`
- Заполните параметры базы данных, Redis, Telegram-токена

4. **Применение миграций и создание суперпользователя:**
``` 
python manage.py migrate
python manage.py csu
```

5. **Запуск Redis (если не запущен):**
``` 
redis-server
```

6. **Запуск Celery worker и beat:**
``` 
celery -A config worker --loglevel=info -P eventlet
celery -A config beat --loglevel=info
```

7. **Запуск сервера:**
``` 
python manage.py runserver
```
## Запуск через Docker

1. **Сборка и запуск контейнеров:**
``` 
docker compose up --build
```
2. **Применение миграций в контейнере:**
``` 
docker compose exec web python manage.py migrate
```
3. **Создание суперпользователя:**
``` 
docker compose exec web python manage.py csu
```
4. **Остановка контейнеров:**
``` 
docker compose down
```

## Функциональности

### Пользователи и права

- Регистрация, аутентификация через JWT.
- Владелец управляет только своими привычками.
- Публичные привычки доступны всем авторизованным пользователям.

### Привычки

- CRUD через DRF.
- Поля: место, время, действие, приятная привычка, связанная привычка, периодичность, вознаграждение, время выполнения, публичность.
- Валидация:
- Нельзя одновременно заполнять `reward` и `related_habit`.
- `execution_time` не больше 120 секунд.
- `related_habit` должна быть приятной.
- У приятной привычки не может быть `reward` или `related_habit`.
- `periodicity` от 1 до 7 дней.

### Пагинация

- 5 привычек на страницу.
- Параметры `page_size` и `page` в запросе.

### Telegram-уведомления

- Каждую минуту Celery отправляет уведомления о привычках в Telegram

### API-документация

- Swagger UI: `/swagger-ui/`
- Redoc: `/redoc/`

## Инструменты

- Python 3.14
- Django 6.0.6
- Django REST Framework 3.17.1
- django-filter 25.2
- djangorestframework-simplejwt 5.5.1
- django-cors-headers 4.9.0
- drf-spectacular 0.30.0
- PostgreSQL (psycopg2-binary 2.9.12)
- Redis 4.6.0
- Celery 5.6.3 + eventlet 0.41.0
- requests 2.34.2
- python-dotenv 1.2.2
- Pillow 12.3.0
- coverage 7.15.0
- ipython 9.15.0
- django-celery-beat 2.9.0
- Poetry
- Docker
