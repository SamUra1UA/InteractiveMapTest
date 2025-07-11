# InteractiveMapTest

Проєкт — вебдодаток на Django для керування та візуалізації локацій на інтерактивній карті. Має автентифікацію користувачів, управління локаціями та REST API для CRUD операцій.

---

## Функціональність

- **Аутентифікація користувачів:** Реєстрація, вхід, профіль, скидання паролю  
- **Управління локаціями:** Додавання, редагування, видалення, перегляд локацій  
- **Інтерактивна карта:** Візуалізація локацій, пошук і фільтрація  
- **REST API:** CRUD операції з даними локацій  

---

## Основні URL та їх призначення

### Веб-інтерфейс

| URL                                  | Опис                                   |
|-------------------------------------|---------------------------------------|
| `/accounts/login/`                   | Сторінка входу користувачів           |
| `/accounts/register/`                | Реєстрація нового користувача         |
| `/accounts/profile/`                 | Профіль користувача                   |
| `/accounts/password_reset/`          | Початок процесу скидання паролю       |
| `/accounts/password_reset_done/`     | Підтвердження відправки листа          |
| `/accounts/password_reset_confirm/<uidb64>/<token>/` | Підтвердження скидання паролю          |
| `/accounts/password_reset_complete/` | Завершення скидання паролю             |
| `/locations/`                       | Список усіх локацій                   |
| `/locations/add/`                   | Додати нову локацію                   |
| `/locations/<pk>/edit/`             | Редагувати локацію                    |
| `/locations/<pk>/delete/`           | Видалити локацію                     |
| `/locations/<pk>/`                  | Деталі локації                        |
| `/map/`                            | Інтерактивна карта                   |
| `/search/`                         | Пошук локацій                        |

---

### API (CRUD для локацій)

| Метод  | URL                     | Опис                           |
|--------|-------------------------|-------------------------------|
| GET    | `/api/locations/`        | Отримати список локацій        |
| POST   | `/api/locations/`        | Створити нову локацію          |
| GET    | `/api/locations/<pk>/`   | Отримати деталі конкретної локації |
| PUT    | `/api/locations/<pk>/`   | Оновити локацію                |
| DELETE | `/api/locations/<pk>/`   | Видалити локацію              |

---

## Як використовувати

1. Клонувати репозиторій:

   ```bash
   git clone https://github.com/SamUra1UA/InteractiveMapTest.git
Встановити залежності:

  ```bash
   pip install -r requirements.txt
   ```
   
Зробити міграції:

  ```bash
python manage.py migrate
```
Запустити сервер розробки:

  ```bash
python manage.py runserver
```
Відкрити у браузері:

```HTTP
http://127.0.0.1:8000/
```
Приклади використання API
Отримати список локацій:

```HTTP
GET http://127.0.0.1:8000/api/locations/
```
Створити локацію:

```http
POST http://127.0.0.1:8000/api/locations/
```
Content-Type: application/json

{
  "name": "Назва локації",
  "description": "Опис",
  "latitude": 50.45,
  "longitude": 30.52,
  ...
}
Отримати деталі локації:

```http
GET http://127.0.0.1:8000/api/locations/1/
```
Оновити локацію:

```http
PUT http://127.0.0.1:8000/api/locations/1/
```
Content-Type: application/json

{
  "name": "Оновлена назва",
  ...
}
Видалити локацію:
```http
DELETE http://127.0.0.1:8000/api/locations/1/