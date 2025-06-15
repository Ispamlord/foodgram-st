# Foodgram Project

## Описание

**Foodgram** — это удобное веб-приложение для всех, кто любит готовить. Оно предоставляет возможность:
- Создавать и публиковать собственные рецепты.
- Изучать кулинарные идеи других пользователей.
- Сохранять любимые рецепты в избранное.
- Формировать список покупок для выбранных блюд.

Проект построен на **Django** и **Django REST Framework** для бэкенда, а фронтенд реализован с использованием **React**.

## Стек технологий

- **Backend**: Python 3, Django, Django REST Framework, PostgreSQL
- **Frontend**: React
- **API**: REST API
- **Контейнеризация**: Docker, Docker Compose
- **Web-сервер**: Nginx

## Инструкция по запуску

Следуйте этим шагам, чтобы развернуть проект локально.

### 1. Клонирование репозитория

Склонируйте репозиторий и перейдите в директорию проекта:

```bash
git clone https://github.com/Ispamlord/foodgram-st.git
cd foodgram-st
```

### 2. Настройка переменных окружения

В папке infra создайте файл .env для настройки переменных окружения:

```bash
cd infra
touch .env
```
Добавьте в файл .env следующие параметры (подставьте свои значения):
```ini
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,foodgram-backend
SECRET_KEY=secret_key
POSTGRES_DB=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodgram
DB_HOST=db
DB_PORT=5432
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=12345
```

### 3. Запуск контейнеров

Из папки infra запустите контейнеры с помощью Docker Compose:
```bash
cd infra
docker compose up -d
```
Это развернет проект с базой данных **PostgreSQL**, бекендом на **Django** и веб-сервером **Nginx**.


### 4. Доступ к проекту

* Главная страница: http://localhost
* Админ-панель Django: http://localhost/admin 
* API документация: http://localhost/api/docs/

### 5. Остановка сервисов
Для остановки контейнеров выполните:
```bash
docker-compose down
```

## Автор

Разработано студентом НГТУ Бульчук Олесей группы АВТ-214