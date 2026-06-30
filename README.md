# ДДС - Веб-сервис для учёта движения денежных средств

Django-приложение для создания, просмотра, редактирования и удаления записей о движении денежных средств.

---

## [СКРИНШОТЫ ПРИЛОЖЕНИЯ](project_demo/SCREENSHOTS.MD)
<p>
    <img src="project_demo/demo-gif.gif" alt="app-photo-4" width="1024">
</p>

---

## Функциональность

- **Главная страница** - таблица всех записей ДДС с итоговыми суммами (пополнения, списания, баланс)
- **Фильтры** - по дате (диапазон), статусу, типу, категории и подкатегории
- **Создание/редактирование записи** - форма с зависимыми выпадающими списками
- **Удаление записи** - форма для удаления записей
- **Управление справочниками** - добавление/редактирование/удаление статусов, типов, категорий и подкатегорий через удобный интерфейс с вкладками

---

## Технологии

- **Backend:** Python 3.14+, Django 5.2.15, Django ORM
- **База данных:** SQLite
- **Frontend:** Bootstrap 5.3, Bootstrap Icons, Vanilla JS

---

## Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/DmitryHook/hh_test_3
cd hh_test_3
```

### 2. Создать виртуальное окружение

```bash
python -m venv .venv
```

**cmd:**
```cmd
.venv\Scripts\activate.bat
```

**PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.venv\Scripts\Activate.ps1
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Применить миграции

```bash
python manage.py migrate
```

### 5. (Опционально) Загрузить тестовые данные

```bash
python manage.py fill_db

Загружает начальные справочники (статусы, типы, категории, подкатегории)
По умолчанию будет создано стандартное количество данных = 50. Чтобы указать своё количество, передайте число аргументом:

python manage.py fill_db {value}
```
где `{value}` - желаемое количество записей (`python manage.py fill_db 100`)

### 6. (Опционально) Создать суперпользователя (для Django Admin)

```bash
python manage.py createsuperuser
```

### 7. Запустить сервер

```bash
python manage.py runserver
```

Приложение доступно по адресу: **http://127.0.0.1:8000/**

Django Admin: **http://127.0.0.1:8000/admin/**

---

## URL-маршруты

| URL | Описание |
|-----|----------|
| `/` | Список записей ДДС |
| `/create/` | Создание новой записи |
| `/<pk>/edit/` | Редактирование записи |
| `/<pk>/delete/` | Удаление записи |
| `/directory/` | Управление справочниками |
| `/api/categories/?type_id=<id>` | категории по типу |
| `/api/subcategories/?category_id=<id>` | подкатегории по категории |

---