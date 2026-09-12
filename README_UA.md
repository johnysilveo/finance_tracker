# Finance Tracker

[English version](README.md)

## 1. Опис проєкту

**Finance Tracker** — це консольний Python-застосунок для керування особистими витратами.

Проєкт створений як **екзаменаційний Variant 3 — Expense Tracking** і використовує багатошарову архітектуру зі SQLite як основним постійним сховищем даних.

Застосунок підтримує:

- керування категоріями;
- керування витратами;
- soft delete та restore;
- валідацію введених даних;
- фільтрацію та аналітичні звіти;
- конструктор звітів;
- конвертацію валют;
- експорт CSV та JSON;
- імпорт CSV та JSON;
- logging;
- генерацію демонстраційних даних через seed.

Архітектура спеціально розділена на шари, щоб у майбутньому можна було додати GUI та повторно використати ту саму бізнес-логіку без переписування роботи з базою даних.

---

## 2. Основні цілі

Проєкт був спроєктований для виконання таких завдань:

1. Створити повноцінний консольний CRUD-застосунок.
2. Використати SQLite як основне сховище даних.
3. Розділити доступ до даних, бізнес-логіку, моделі та CLI.
4. Валідовувати дані до їх запису в базу.
5. Зберігати зв'язок між витратами та категоріями.
6. Реалізувати корисні звіти по витратах.
7. Експортувати звіти у CSV та JSON.
8. Підтримати імпорт витрат з CSV та JSON.
9. Додати soft delete та restore.
10. Додати logging як бонусну функціональність.
11. Додати seed-дані для демонстрації та тестування.
12. Зберегти архітектуру придатною для майбутнього GUI.

---

## 3. Технології

- **Python 3.10+**
- **SQLite**
- Стандартна бібліотека Python:
  - `sqlite3`
  - `dataclasses`
  - `datetime`
  - `decimal`
  - `csv`
  - `json`
  - `pathlib`
  - `logging`
  - `urllib`
  - `re`
  - `random`
  - `time`
- **Публічний currency API Monobank**
- **Git / GitHub**

Поточна реалізація не потребує сторонніх Python-пакетів.

---

## 4. Архітектура

Проєкт використовує багатошарову архітектуру:

```text
CLI
 ↓
Services
 ↓
Repositories
 ↓
SQLite Database
```

Додаткові модулі:

```text
Models      -> представляють дані застосунку
Validators  -> перевіряють і нормалізують введення
Currency    -> завантажує та застосовує курси валют
Export      -> записує звіти в CSV/JSON
Import      -> читає витрати з CSV/JSON
Logging     -> записує важливі події застосунку
Seed        -> генерує демонстраційні дані
```

Майбутній GUI зможе використовувати той самий backend:

```text
CLI ──┐
      ├──> Services -> Repositories -> SQLite
GUI ──┘
```

Таке розділення не дозволяє змішувати інтерфейс, SQL та бізнес-правила в одному місці.

---

## 5. Структура проєкту

```text
Finance_tracker/
├── database/
│   ├── __init__.py
│   ├── db.py
│   └── finence.db
│
├── models/
│   ├── __init__.py
│   ├── category.py
│   └── expense.py
│
├── repositories/
│   ├── __init__.py
│   ├── category_repository.py
│   ├── expense_repository.py
│   └── report_repository.py
│
├── services/
│   ├── __init__.py
│   ├── category_service.py
│   ├── expense_service.py
│   ├── report_service.py
│   ├── currency_service.py
│   ├── report_storage.py
│   ├── export_service.py
│   └── import_service.py
│
├── cli/
│   ├── __init__.py
│   ├── console_ui.py
│   ├── category_menu.py
│   ├── expense_menu.py
│   ├── report_menu.py
│   ├── custom_report_menu.py
│   ├── import_menu.py
│   └── main_manu.py
│
├── utils/
│   ├── __init__.py
│   ├── validators.py
│   └── logger.py
│
├── exports/
├── logs/
├── main.py
├── seed.py
├── .gitignore
└── README.md
```

> `finence.db` — поточна назва файлу бази даних у проєкті.

> `main_manu.py` — поточна назва файлу, який імпортується у `main.py`. Якщо пізніше файл буде перейменований у `main_menu.py`, потрібно одночасно змінити import та структуру в README.

---

## 6. Відповідальність шарів

### `database/`

Містить підключення до SQLite та ініціалізацію бази.

`db.py`:

- задає шлях до БД;
- відкриває SQLite connection;
- вмикає foreign keys;
- створює необхідні таблиці;
- централізує налаштування БД.

### `models/`

Містить dataclass-моделі.

Поточні моделі:

- `Category`
- `Expense`

Моделі представляють дані та не виконують SQL напряму.

### `repositories/`

Відповідають за доступ до бази даних.

Repository містить SQL для:

- create;
- read;
- update;
- soft delete;
- restore;
- отримання даних для звітів.

Repository не працює з консольним input.

### `services/`

Містять бізнес-логіку.

Service layer:

- перевіряє бізнес-правила;
- координує repositories;
- конвертує дати;
- перевіряє зв'язок з категоріями;
- виконує конвертацію валют;
- будує звіти;
- обробляє import/export;
- записує важливі операції в log.

### `cli/`

Містить меню та консольний інтерфейс.

CLI:

- показує меню;
- читає вибір користувача;
- викликає services;
- виводить результати;
- підтримує Back/Cancel.

### `utils/`

Містить спільні допоміжні компоненти:

- validators;
- navigation exceptions;
- logger.

---

## 7. Структура бази даних

Застосунок використовує SQLite.

Файл бази:

```text
database/finence.db
```

### Таблиця Categories

```sql
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    is_deleted INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

### Таблиця Expenses

```sql
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL REFERENCES categories(id),
    name TEXT NOT NULL,
    currency TEXT NOT NULL DEFAULT 'USD',
    amount_cents INTEGER NOT NULL CHECK(amount_cents > 0),
    date TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    is_deleted INTEGER DEFAULT 0,
    description TEXT
);
```

### Зв'язок

Кожна витрата належить одній категорії:

```text
Category 1 ───────< many Expenses
```

Foreign key:

```text
expenses.category_id -> categories.id
```

SQLite foreign keys вмикаються через:

```sql
PRAGMA foreign_keys = ON;
```

---

## 8. Models

### Category

Основні поля:

```text
id
name
description
is_deleted
created_at
updated_at
```

### Expense

Основні поля:

```text
id
name
date
amount_cents
category_id
currency
description
is_deleted
created_at
updated_at
```

Суми зберігаються як цілі cents, а не `float`.

Приклад:

```text
$156.60 -> 15660 cents
```

Це дозволяє уникнути типових проблем точності floating-point при фінансових розрахунках.

---

## 9. Функціональність Categories

Підтримуються:

- створення категорії;
- перегляд активних категорій;
- перегляд деталей;
- оновлення;
- soft delete;
- перегляд видалених категорій;
- restore;
- перевірка duplicate category name.

Назва категорії є унікальною.

---

## 10. Функціональність Expenses

Підтримуються:

- створення expense;
- перегляд усіх активних expenses;
- перегляд деталей;
- update;
- soft delete;
- перегляд deleted expenses;
- restore.

Expense містить:

- name;
- date;
- category;
- amount;
- currency;
- optional description.

Перед створенням або оновленням Expense Service перевіряє, що вибрана категорія існує.

---

## 11. Soft Delete

Categories та Expenses використовують soft delete.

Замість фізичного видалення рядка:

```text
is_deleted = 1
```

Restore змінює значення назад:

```text
is_deleted = 0
```

Переваги:

- запис можна відновити;
- історія даних зберігається;
- випадкове видалення не знищує інформацію фізично.

---

## 12. Валідація

Спільна валідація знаходиться у:

```text
utils/validators.py
```

Перевіряються:

- positive integer ID;
- non-empty name;
- optional description;
- positive amount;
- максимум 2 decimal places;
- supported currency;
- реальна календарна дата;
- numeric menu values.

### Amount

Дозволено:

```text
10
10.5
10.50
156.60
```

Не дозволено:

```text
0
-10
10.555
abc
```

Перед записом amount конвертується в cents.

### Date

CLI приймає різні separators.

Приклади:

```text
26-3-5
26/3/5
26.3.5
26'3'5
```



Формат у database:

```text
2026-03-05
```

Таким чином дати у БД зберігаються у sortable ISO format.

---

## 13. CLI Navigation

Спільні правила навігації:

```text
B = Back
X = Cancel
```

Поведінка:

- `B` повертає до попереднього поля;
- `B` у першому полі виходить з поточної операції;
- `X` скасовує всю операцію;
- неправильне значення не переводить користувача далі — те саме поле запитується повторно.

Ця поведінка використовується в Categories, Expenses, Reports та Import.

---

## 14. Reports

Архітектура reports:

```text
Report CLI
    ↓
Report Service
    ↓
Report Repository
    ↓
SQLite
```

Repository отримує raw expense rows.

Service виконує:

- filtering;
- currency normalization;
- aggregation;
- minimum/maximum;
- category totals;
- average calculations.

Поточний report system містить 13 report modes плюс Custom Report Builder.

Підтримуються такі типи аналітики:

- filter expenses by category;
- filter expenses by name;
- filter expenses by date range;
- maximum expense;
- minimum expense;
- calculations by category;
- calculations by period;
- totals by category;
- top spending category;
- average daily spending.

Це покриває обов'язкові звіти та додає розширену аналітику.

---

## 15. Custom Report Builder

Custom Report Builder дозволяє об'єднати кілька report sections в один report.

Workflow:

```text
Choose number of sections
        ↓
Choose report sections
        ↓
Choose target currency
        ↓
Build report
        ↓
Store as last report
        ↓
Display / Export
```

Якщо користувач запитує всі 11 sections, застосунок автоматично вибирає всі report sections і не змушує вводити 11 виборів вручну.

Останній generated report зберігається в RAM через:

```text
services/report_storage.py
```

Він доступний до закриття застосунку.

Експортовані файли залишаються на диску.

---

## 16. Currency Conversion

Підтримуються:

```text
USD
EUR
UAH
```

Дані отримуються з:

```text
Monobank public currency API
https://api.monobank.ua/bank/currency
```

Service використовує 5-minute cache:

```text
CACHE_SECONDS = 300
```

Це дозволяє не викликати API для кожної expense.

Conversion flow:

```text
Source currency
      ↓
     UAH
      ↓
Target currency
```

Приклад:

```text
USD -> UAH -> EUR
```

Для фінансового rounding використовуються:

```text
Decimal
ROUND_HALF_UP
```

### Важливе обмеження

Застосунок використовує **поточний курс Monobank** при побудові converted reports.

Historical exchange rates за датою expense не зберігаються.

Тому історична expense при конвертації сьогодні може мати результат, який відрізняється від реального курсу на дату цієї витрати.

---

## 17. Export

Reports можна експортувати у:

- JSON;
- CSV.

Service:

```text
services/export_service.py
```

Directory:

```text
exports/
```

Папка створюється автоматично під час першого export.

Filename містить timestamp:

```text
finance_report_2026-09-07_10-30-15.json
finance_report_2026-09-07_10-30-15.csv
```

### JSON

JSON зберігає повну структуру report.

### CSV

Оскільки різні sections можуть мати різну структуру, використовується універсальний CSV формат:

```text
section_number
section_title
parameters
row_number
display_line
data
```

Structured values при необхідності записуються як JSON text усередині CSV cell.

---

## 18. Import

Застосунок підтримує import expenses з:

- CSV;
- JSON.

Service:

```text
services/import_service.py
```

### CSV example

```csv
name,category,amount,currency,date,description
Walmart,Groceries,125.50,USD,09/01/2026,Weekly groceries
Shell,Fuel,64.20,USD,09/02/2026,Fuel
```

Category також можна передати через `category_id`.

### JSON example

```json
[
    {
        "name": "Walmart",
        "category": "Groceries",
        "amount": 125.50,
        "currency": "USD",
        "date": "09/01/2026",
        "description": "Weekly groceries"
    }
]
```

### Поведінка import

Кожен imported row проходить через звичайний Expense Service.

Тому import повторно використовує:

- date validation;
- amount validation;
- category relationship checks;
- currency restrictions;
- database rules.

Неправильний рядок не зупиняє весь import — він записується до списку errors.

### Поточне обмеження import

Поточна функція імпортує **expenses**.

Категорії, на які посилаються imported expenses, повинні вже існувати в database.

---

## 19. Logging

Logging реалізований у:

```text
utils/logger.py
```

Log file:

```text
logs/finance_tracker.log
```

Логуються:

- application start;
- application close;
- unexpected exceptions;
- category create/update/delete/restore;
- expense create/update/delete/restore;
- report export;
- import start та summary;
- failed import rows;
- Monobank connection/data errors;
- successful currency-rate loading.

Рівні:

```text
INFO     нормальна операція
WARNING  recoverable problem
ERROR    operation/API/file problem
EXCEPTION unexpected crash + traceback
```

Приклад:

```text
2026-09-07 10:42:03 | INFO | Expense created: ID=4321, name=Shell, amount_cents=6540, currency=USD, category_id=3
2026-09-07 10:43:44 | WARNING | Import row failed: row=3, error=Invalid date
2026-09-07 10:44:20 | INFO | Report exported to JSON: ...
```

Runtime `.log` files краще не комітити.

Recommended `.gitignore`:

```gitignore
logs/*.log
```

Якщо треба зберегти саму папку `logs/` у Git, в неї можна додати:

```text
.gitkeep
```

---

## 20. Seed Data

Demo data створюються командою:

```bash
python seed.py
```

Seed script:

- ініціалізує БД за потреби;
- створює відсутні categories;
- генерує demo expenses;
- покриває останні 36 місяців;
- створює 10 expenses на кожну category щомісяця;
- використовує `random.seed(42)`;
- не дублює власні seed rows при повторному запуску.

Категорії:

1. Groceries
2. Restaurants
3. Fuel
4. Hotels
5. Entertainment
6. Car maintenance
7. Shopping
8. Phone/Home Internet
9. Lease/Auto Loan
10. Rent/Mortgage
11. Subscriptions
12. Uncategorized

Очікувана кількість expenses:

```text
12 categories × 5 expenses = 60 expenses
Date range: 03/01/2026 → current date
```



Перший запуск:

```text
Seed completed successfully
Categories: 12
Expenses created: 60
Expenses skipped: 0
Expected seed expenses: 60
```

Повторний запуск повинен skip existing seed rows замість створення duplicates.

---

## 21. Application Startup

Entry point:

```text
main.py
```

При запуску:

1. у log записується `Application started`;
2. викликається `init_db()`;
3. відкривається main menu;
4. unexpected exception ловиться на top level;
5. traceback записується через logger;
6. при завершенні записується `Application closed`.

---

## 22. Встановлення та запуск

### Clone repository

```bash
git clone https://github.com/johnysilveo/finance_tracker.git
cd finance_tracker
```

### Запустити application

```bash
python main.py
```

Database tables створюються автоматично.

### Додати demo data

```bash
python seed.py
```

Після цього:

```bash
python main.py
```

Сторонні packages для поточної реалізації не потрібні.

---


## 23. Рекомендований сценарій демонстрації


На захисті можна показати:


1. Запуск application.

2. Categories.

3. Create category.

4. Update category.

5. Soft delete.

6. Deleted Categories.

7. Restore.

8. Create expense.

9. Update expense.

10. Soft delete та restore expense.

11. Кілька reports.

12. Custom Report.

13. Export JSON.

14. Export CSV.

15. Import невеликого CSV або JSON.

16. Відкрити `logs/finance_tracker.log`.

17. Показати, що операції були записані.

18. Показати SQLite database.

19. Повторно запустити `seed.py` та показати, що seed data не дублюються.


---

# План розробки / Як був побудований проєкт

Цей розділ описує послідовність, у якій проєкт проєктувався та реалізовувався.

## Крок 1 — Визначення задачі

Спочатку був розібраний Expense Tracking exam variant.

Основні entities:

```text
Category
Expense
```

Relationship:

```text
Expense -> Category
```

Обов'язкові вимоги:

```text
CRUD
Validation
Reports
SQLite
CSV/JSON export
Console menus
```

Додатково були заплановані:

```text
Soft delete
Restore
Currency conversion
Custom reports
Import
Logging
Seed data
```

---

## Крок 2 — Проєктування архітектури

До реалізації всіх функцій застосунок був розділений на:

```text
Models
Repositories
Services
CLI
Database
Utilities
```

Причини:

- SQL не повинен бути змішаний з menu code;
- validation не повинна дублюватися;
- business logic повинна повторно використовуватися;
- майбутній GUI повинен мати можливість використовувати Services.

Основний flow:

```text
User
 ↓
CLI
 ↓
Service
 ↓
Repository
 ↓
SQLite
```

---

## Крок 3 — SQLite Database

Був створений:

```text
database/db.py
```

Його задачі:

- визначити `DB_PATH`;
- створювати connections;
- вмикати foreign keys;
- створювати `categories`;
- створювати `expenses`.

Після цього SQLite стала primary source of truth.

---

## Крок 4 — Models

Були створені dataclass:

```text
Category
Expense
```

Вони використовуються для структурованої передачі даних між Repository, Service та CLI.

---

## Крок 5 — Category Repository

Спочатку був реалізований repository для categories.

Operations:

- create;
- get by ID;
- get by name;
- list;
- update;
- soft delete;
- restore;
- list deleted.

Це створило перший повний persistence layer.

---

## Крок 6 — Category Service

Над repository були додані business rules:

- name не може бути empty;
- duplicate category заборонений;
- ID повинен бути valid;
- missing category генерує error;
- CLI не працює з SQL напряму.

---

## Крок 7 — Category CLI

Було додано category menu:

```text
Add
Show All
Update
Delete
Restore
Details
Show Deleted
Back
```

Так був завершений перший end-to-end flow:

```text
CLI -> Service -> Repository -> SQLite
```

---

## Крок 8 — Expense Repository

Той самий architecture pattern був застосований до expenses.

Operations:

- create;
- get active expense;
- get all active;
- update;
- soft delete;
- restore;
- get deleted.

---

## Крок 9 — Expense Service

Були додані business rules:

- required name;
- positive amount;
- valid date;
- valid category;
- normalized currency;
- conversion UI date -> DB date.

Amount зберігається у cents.

Date зберігається в ISO format.

---

## Крок 10 — Expense CLI

Було додано expense menu:

```text
Add
Show All
Update
Delete
Restore
Details
Show Deleted
Back
```

CLI дозволяє вибрати existing category для expense.

---

## Крок 11 — Shared Validators

Повторюваний input code був винесений у:

```text
utils/validators.py
```

Були створені validators для:

- ID;
- names;
- descriptions;
- amounts;
- dates;
- currencies;
- menu numbers.

Також були додані:

```text
PreviousField
CancelOperation
```

Це забезпечило спільну B/X navigation.

---

## Крок 12 — Shared Console UI

Спільний UI code був винесений у:

```text
cli/console_ui.py
```

Модуль містить:

- border;
- centered output;
- centered input;
- headers;
- wait/pause.

Це зробило CLI візуально послідовним.

---

## Крок 13 — Report Repository

Report repository був залишений відповідальним лише за отримання raw expenses.

Він отримує expenses по:

- category;
- name;
- date range.

Aggregation навмисно не виконується SQL-запитом для mixed currencies.

---

## Крок 14 — Currency Service

Було додано currency conversion через Monobank.

Ключове architecture decision:

```text
Не викликати API для кожної expense.
```

Замість цього:

1. rates завантажуються один раз;
2. кешуються на 5 хвилин;
3. reuse для всього report;
4. conversion проходить через UAH;
5. aggregation виконується після conversion.

---

## Крок 15 — Report Service

Report Service об'єднав:

```text
raw expenses + currency rates + calculations
```

Тут реалізуються:

- max;
- min;
- totals;
- top category;
- average daily spending.

Аналітика не знаходиться ні у CLI, ні у Repository.

---

## Крок 16 — Report CLI

Було додано report menu.

Користувач може передавати:

- category;
- name;
- date range;
- target currency.

Після цього результати форматуються та показуються в console.

---

## Крок 17 — Custom Report Builder

Було створено Custom Report Builder.

Користувач вибирає:

```text
number of sections
report types
target currency
```

Report зберігається як last report.

Якщо вибрані всі 11 sections, застосунок автоматично додає всі report types.

---

## Крок 18 — Report Storage

Було створено:

```text
services/report_storage.py
```

Його мета:

- розділити generation та export;
- дозволити exporter використати last report;
- не створювати окрему database table для temporary state.

---

## Крок 19 — CSV/JSON Export

Було створено:

```text
services/export_service.py
```

Функціональність:

- автоматичне створення `exports/`;
- timestamp filenames;
- full JSON export;
- universal CSV export.

Exporter працює з готовим report object.

---

## Крок 20 — CSV/JSON Import

Були створені:

```text
services/import_service.py
cli/import_menu.py
```

Підтримуються:

```text
CSV
JSON
```

Imported expense проходить через існуючий Expense Service, а не вставляється напряму в database.

Це повторно використовує validation.

---

## Крок 21 — Seed Data

Було створено:

```text
seed.py
```

Він генерує:

```text
12 categories
10 expenses/category/month
36 months
4320 expenses
```

Seed marker дозволяє безпечно запускати script повторно.

---

## Крок 22 — Logging

Було створено:

```text
utils/logger.py
```

Logging підключений до:

- `main.py`;
- Category Service;
- Expense Service;
- Import Service;
- Export Service;
- Currency Service.

Read operations навмисно не логуються, щоб log не був забитий непотрібними записами.

---

## Крок 23 — Final Integration

Фінальний flow:

```text
main.py
 ↓
init_db()
 ↓
main menu
 ├── Categories
 ├── Expenses
 ├── Reports / Exports
 └── Import
```

Додатково використовуються:

```text
SQLite
Monobank API
CSV / JSON
Logging
Seed data
```

---

## 24. Основні design decisions

### Чому Services?

Service layer містить business logic та не дозволяє CLI напряму керувати database.

### Чому Repositories?

Repository ізолює SQL.

### Чому cents?

Integer cents дозволяють уникнути floating-point errors.

### Чому ISO dates у DB?

`YYYY-MM-DD` легко сортувати та фільтрувати.

### Чому soft delete?

Дані можна restore, і history не знищується фізично.

### Чому current exchange rate?

Проєкт не підтримує historical exchange-rate database, тому для reports використовується поточний Monobank rate.

### Чому rate cache?

Report може містити тисячі expenses. Один API request значно ефективніший за request для кожної expense.

### Чому Import використовує Expense Service?

Imported data не повинні обходити validation.

### Чому не логуються всі READ operations?

Logging повинен показувати важливі changes та problems, а не створювати тисячі непотрібних записів.

---

## 25. Error Handling

Expected errors обробляються на відповідному рівні.

Приклади:

- invalid ID;
- invalid date;
- invalid amount;
- missing category;
- missing expense;
- duplicate category;
- unsupported currency;
- missing import file;
- invalid JSON;
- invalid CSV row;
- Monobank network error.

Unexpected top-level errors логуються у `main.py` разом з traceback.

---

## 26. Поточні обмеження

1. Застосунок консольний.
2. Currency conversion використовує current rate, а не historical.
3. Last custom report зберігається лише в RAM.
4. Import expenses потребує existing categories.
5. SQLite використовується як local single-file database.
6. Seed data є demo data, а не реальною фінансовою історією.

---

## 27. Можливі майбутні покращення

- desktop GUI;
- historical currency rates;
- charts;
- dashboard;
- budgets;
- recurring expenses;
- user accounts;
- authentication;
- database migrations;
- unit tests;
- integration tests;
- more currencies;
- advanced import mapping;
- report history в SQLite;
- PDF export.

Поточна architecture дозволяє додавати ці можливості без переписування core layers.

---

## 28. Git Workflow

Repository:

```text
https://github.com/johnysilveo/finance_tracker.git
```

Branches:

```text
main
dev
```

Workflow:

```text
development on dev
        ↓
test
        ↓
merge into main
```

---

## 29. Final Project Checklist

Перед здачею:

- [ ] `python main.py` запускається без errors
- [ ] database initializes automatically
- [ ] Category CRUD працює
- [ ] Category soft delete/restore працює
- [ ] Expense CRUD працює
- [ ] Expense soft delete/restore працює
- [ ] validation reject bad data
- [ ] усі report modes працюють
- [ ] Custom Report Builder працює
- [ ] USD/EUR/UAH conversion працює
- [ ] Monobank failure обробляється
- [ ] CSV report export працює
- [ ] JSON report export працює
- [ ] CSV expense import працює
- [ ] JSON expense import працює
- [ ] invalid import rows показуються
- [ ] `python seed.py` працює
- [ ] repeated seed не дублює seed data
- [ ] logging file створюється
- [ ] CRUD writes з'являються у log
- [ ] export/import events з'являються у log
- [ ] README відповідає final code
- [ ] `.gitignore` виключає runtime/generated files де потрібно
- [ ] final tested version закомічена в GitHub

---

## 30. Підсумок

Finance Tracker — це повноцінний layered Python expense-tracking application, який демонструє:

```text
Python
SQLite
CRUD
Validation
Reports
Currency Conversion
CSV / JSON Import
CSV / JSON Export
Soft Delete
Logging
Seed Data
```

Проєкт демонструє separation of concerns, relational database relationships, validation, persistence, API integration, reporting, file processing та maintainable application architecture.
