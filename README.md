# Todo with Auth

Backend API для TODO-приложения на FastAPI с JWT-аутентификацией, PostgreSQL и разделением прав между обычными пользователями и администраторами.

Проект учебный, старался правильно разбить на роутеры, сервисный слой, DAO, схемы, модели и миграции.

---

## Как запустить локально
### 1. Клонировать репозиторий
- git clone https://github.com/hornum/todo-with-auth.git
- cd todo-with-auth
### 2. Создать виртуальное окружение
- python -m venv .venv

#### Windows:
- .venv\Scripts\activate
#### Linux / macOS:
- source .venv/bin/activate

### 3. Установить зависимости
- pip install -r requirements.txt

### 4. Создать .env

В проекте есть .env.example

### 5. Применить миграции
alembic upgrade head

### 6. Запустить приложение
uvicorn app.main:app --reload

После запуска документация будет доступна по адресу: http://127.0.0.1:8000/docs

---

## Стек

- Python
- FastAPI
- SQLAlchemy Async
- PostgreSQL
- Alembic
- JWT (`python-jose`)

---

## Возможности

### Аутентификация
- регистрация пользователя
- вход по username + password
- выдача JWT

### Пользовательские функции
- получить данные текущего пользователя "/me"
- создать задачу
- получить список своих задач
- получить задачу по id
- изменить статус задачи (Сделана/Не сделана)
- удалить одну задачу
- удалить все свои задачи
- сменить пароль

### Админские функции
- посмотреть все задачи
- получить пользователя по id
- удалить задачу любого юзера по ID
- создать задачу для другого пользователя
- выдать или снять права администратора

---

## Основные роуты
### Auth
- POST /auth/register
- POST /auth/token
### Users
- GET /users/me
- POST /users/password
### Tasks
- GET /tasks/
- GET /tasks/{task_id}
- POST /tasks/
- PATCH /tasks/{task_id}/status
- DELETE /tasks/{task_id}
- DELETE /tasks/
### Admin
- GET /admin/todos
- GET /admin/users/{user_id}
- DELETE /admin/todos/{task_id}
- POST /admin/todos/{target_user_id}
- PATCH /admin/users/role/{user_id}

---

## Структура проекта

```text
app/
├── routers/
│   ├── admin.py
│   ├── auth.py
│   ├── tasks.py
│   └── users.py
├── admin_service.py
├── config.py
├── dao.py
├── database.py
├── main.py
├── models.py
├── schemas.py
└── service.py
```

---

Планы
- Фильтрация и сортировка задач
- Пагинация
- Тесты
- Refresh token
- Doker / docker-compose + Обновить readme под него