# Finance Tracker

[Українська версія](README_UA.md)

## 1. Project Overview

**Finance Tracker** is a console-based Python application for managing personal expenses.

The project was built as **Exam Variant 3 — Expense Tracking** and uses a layered architecture with SQLite as the primary persistent storage.

The application supports:

- category management;
- expense management;
- soft delete and restore;
- input validation;
- filtering and analytical reports;
- report building;
- currency conversion;
- CSV and JSON export;
- CSV and JSON import;
- logging;
- demo database seeding.

The application is intentionally separated into layers so that another user interface, such as a GUI, can later reuse the same business logic without rewriting the database layer.

---

## 2. Main Goals

The project was designed to satisfy the following goals:

1. Build a complete console CRUD application.
2. Use SQLite as the main data storage.
3. Separate data access, business logic, models, and CLI code.
4. Validate user input before storing data.
5. Preserve relationships between expenses and categories.
6. Produce useful expense reports.
7. Export report data to CSV and JSON.
8. Support CSV and JSON expense import.
9. Add soft delete and restore operations.
10. Add logging as an additional feature.
11. Add seed data for demonstration and testing.
12. Keep the architecture reusable for a future GUI.

---

## 3. Technology Stack

- **Python 3.10+**
- **SQLite**
- Python standard library:
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
- **Monobank public currency API**
- **Git / GitHub**

No third-party Python package is required by the current implementation.

---

## 4. Architecture

The project uses a layered architecture:

```text
CLI
 ↓
Services
 ↓
Repositories
 ↓
SQLite Database
```

Additional supporting modules:

```text
Models      -> represent application data
Validators  -> validate and normalize user input
Currency    -> loads and applies currency rates
Export      -> writes reports to CSV/JSON
Import      -> reads expense data from CSV/JSON
Logging     -> stores important application events
Seed        -> generates demonstration data
```

A future GUI can reuse the same backend:

```text
CLI ──┐
      ├──> Services -> Repositories -> SQLite
GUI ──┘
```

This separation keeps interface code independent from persistence and business rules.

---

## 5. Project Structure

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

> `finence.db` is the database filename currently used by the project.

> `main_manu.py` is the current filename imported by `main.py`. If it is later renamed to `main_menu.py`, the import and this structure should be updated together.

---

## 6. Layer Responsibilities

### `database/`

Contains SQLite connection and database initialization logic.

`db.py`:

- defines the database path;
- opens SQLite connections;
- enables foreign keys;
- creates required tables;
- keeps database setup in one place.

### `models/`

Contains dataclasses representing application entities.

Current models:

- `Category`
- `Expense`

Models contain data only and do not directly execute SQL.

### `repositories/`

Responsible for database access.

Repositories contain SQL for:

- create;
- read;
- update;
- soft delete;
- restore;
- report data retrieval.

The repository layer does not handle console input.

### `services/`

Contains application business logic.

Services:

- validate business rules;
- coordinate repositories;
- convert dates;
- check category relationships;
- perform currency conversion;
- build report results;
- process imports and exports;
- log important operations.

### `cli/`

Contains console menus and display/input logic.

The CLI:

- shows menus;
- reads user choices;
- calls services;
- displays results;
- supports Back/Cancel navigation.

### `utils/`

Contains reusable utilities:

- input validators;
- custom navigation exceptions;
- application logger.

---

## 7. Database Design

The application uses SQLite.

Database file:

```text
database/finence.db
```

### Categories table

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

### Expenses table

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

### Relationship

Each expense belongs to one category:

```text
Category 1 ───────< many Expenses
```

The foreign key is:

```text
expenses.category_id -> categories.id
```

SQLite foreign key enforcement is enabled with:

```sql
PRAGMA foreign_keys = ON;
```

---

## 8. Models

### Category

Main fields:

```text
id
name
description
is_deleted
created_at
updated_at
```

### Expense

Main fields:

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

Amounts are stored as integer cents instead of floating-point values.

Example:

```text
$156.60 -> 15660 cents
```

This avoids common floating-point precision problems in financial calculations.

---

## 9. Category Features

The application supports:

- create category;
- show all active categories;
- show category details;
- update category;
- soft delete category;
- show deleted categories;
- restore category;
- duplicate-name validation.

Category names are unique.

---

## 10. Expense Features

The application supports:

- create expense;
- show all active expenses;
- show expense details;
- update expense;
- soft delete expense;
- show deleted expenses;
- restore expense.

Each expense contains:

- name;
- date;
- category;
- amount;
- currency;
- optional description.

Before an expense is created or updated, the service verifies that the selected category exists.

---

## 11. Soft Delete

Categories and expenses use soft delete.

Instead of physically removing a row from the database:

```text
is_deleted = 1
```

Restoring the record changes it back to:

```text
is_deleted = 0
```

Benefits:

- deleted data can be recovered;
- database history is preserved;
- accidental deletion is less destructive.

---

## 12. Input Validation

Validation is centralized in:

```text
utils/validators.py
```

Validation includes:

- positive integer IDs;
- non-empty names;
- optional descriptions;
- positive monetary amounts;
- maximum two decimal places for amounts;
- supported currencies;
- valid calendar dates;
- numeric menu selections.

### Amount validation

Accepted:

```text
10
10.5
10.50
156.60
```

Rejected:

```text
0
-10
10.555
abc
```

The input is converted to cents before storage.

### Date validation

The console accepts flexible separators.

Examples:

```text
3/5/26
3-5-26
3.5.26
3'5'26
```

Normalized UI result:

```text
03/05/2026
```

Database format:

```text
2026-03-05
```

The database therefore keeps dates sortable using ISO format.

---

## 13. CLI Navigation

The CLI uses shared navigation rules:

```text
B = Back
X = Cancel
```

Behavior:

- `B` returns to the previous field during multi-step input;
- `B` on the first field exits the current operation;
- `X` cancels the complete operation;
- invalid values are rejected immediately and the same field is requested again.

This behavior is shared between Categories, Expenses, Reports, and Import workflows.

---

## 14. Reports

The reporting system is separated into:

```text
Report CLI
    ↓
Report Service
    ↓
Report Repository
    ↓
SQLite
```

The repository retrieves raw expense records.

The service performs:

- filtering;
- currency normalization;
- aggregation;
- minimum/maximum calculations;
- category totals;
- average calculations.

The current report system contains 11 report modes plus the Custom Report Builder.

Supported report functionality includes:

- filter expenses by category;
- filter expenses by name;
- filter expenses by date range;
- maximum expense calculations;
- minimum expense calculations;
- calculations by category;
- calculations by period;
- totals by category;
- top spending category;
- average daily spending.

This satisfies the requirement for multiple analytical reports and also provides additional report functionality.

---

## 15. Custom Report Builder

The Custom Report Builder allows the user to combine multiple report sections into one report.

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

If all 11 report sections are requested, the application automatically selects every report section instead of asking for all 11 individually.

The last generated custom report is kept in memory through:

```text
services/report_storage.py
```

The in-memory report is available until the application closes.

Exported files remain on disk.

---

## 16. Currency Conversion

Supported currencies:

```text
USD
EUR
UAH
```

Currency data is loaded from:

```text
Monobank public currency API
https://api.monobank.ua/bank/currency
```

The service uses a five-minute cache:

```text
CACHE_SECONDS = 300
```

This avoids calling the API for every expense.

Conversion logic:

```text
Source currency
      ↓
     UAH
      ↓
Target currency
```

Example:

```text
USD -> UAH -> EUR
```

The service uses `Decimal` and `ROUND_HALF_UP` for financial rounding.

### Important limitation

The application uses the **current Monobank exchange rate** when generating converted reports.

It does **not** store historical exchange rates for the original expense date.

Therefore a historical expense converted today may produce a different result than the exchange rate that existed when the expense occurred.

---

## 17. Export

Reports can be exported to:

- JSON;
- CSV.

Export service:

```text
services/export_service.py
```

Export directory:

```text
exports/
```

The directory is created automatically when the first export is performed.

Generated filenames contain a timestamp:

```text
finance_report_2026-09-07_10-30-15.json
finance_report_2026-09-07_10-30-15.csv
```

### JSON

JSON preserves the complete report structure.

### CSV

Because different report sections may have different structures, CSV uses a universal structure:

```text
section_number
section_title
parameters
row_number
display_line
data
```

Structured values are serialized into JSON text where required.

---

## 18. Import

The application supports expense import from:

- CSV;
- JSON.

Import service:

```text
services/import_service.py
```

### CSV example

```csv
name,category,amount,currency,date,description
Walmart,Groceries,125.50,USD,09/01/2026,Weekly groceries
Shell,Fuel,64.20,USD,09/02/2026,Fuel
```

A category can also be referenced by `category_id`.

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

### Import behavior

Every imported row still passes through the normal expense service.

Therefore imported data uses the same:

- date validation;
- amount validation;
- category relationship checks;
- currency restrictions;
- database rules.

Invalid rows are reported without stopping the entire import.

### Current import limitation

The current import feature imports **expenses**.

Categories referenced by the imported expenses must already exist in the database.

---

## 19. Logging

Logging is implemented through:

```text
utils/logger.py
```

Log file:

```text
logs/finance_tracker.log
```

Logged events include:

- application start;
- application close;
- unexpected application exceptions;
- category create/update/delete/restore;
- expense create/update/delete/restore;
- report export;
- import start and summary;
- failed import rows;
- Monobank connection/data problems;
- successful currency-rate loading.

Log levels:

```text
INFO     normal application operation
WARNING  recoverable problem
ERROR    operation/API/file problem
EXCEPTION unexpected application crash with traceback
```

Example:

```text
2026-09-07 10:42:03 | INFO | Expense created: ID=4321, name=Shell, amount_cents=6540, currency=USD, category_id=3
2026-09-07 10:43:44 | WARNING | Import row failed: row=3, error=Invalid date
2026-09-07 10:44:20 | INFO | Report exported to JSON: ...
```

Runtime `.log` files should normally be ignored by Git.

Recommended `.gitignore` rule:

```gitignore
logs/*.log
```

A `.gitkeep` file may be placed inside `logs/` if the empty directory must remain visible in the repository.

---

## 20. Seed Data

Demo data can be generated using:

```bash
python seed.py
```

The seed script:

- initializes the database if required;
- creates missing categories;
- generates test expenses;
- covers the last 36 months;
- creates 10 expenses per category per month;
- uses deterministic random generation with `random.seed(42)`;
- avoids duplicating its own generated records on repeated runs.

Current seed categories:

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

Total expected seeded expenses:

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

A repeated run should skip already generated seed rows instead of creating duplicates.

---

## 21. Application Startup

Main entry point:

```text
main.py
```

The application:

1. writes `Application started` to the log;
2. initializes the database;
3. starts the main menu;
4. catches unexpected application errors;
5. logs a traceback for an unexpected failure;
6. writes `Application closed` when execution ends.

---

## 22. Installation and Run

### Clone the repository

```bash
git clone https://github.com/johnysilveo/finance_tracker.git
cd finance_tracker
```

### Run the application

```bash
python main.py
```

The database tables are initialized automatically.

### Add demo data

```bash
python seed.py
```

Then start the application again:

```bash
python main.py
```

No external package installation is currently required.

---

## 23. Recommended Demo Sequence

For a project demonstration:

1. Run the application.
2. Show Categories.
3. Create a new category.
4. Update the category.
5. Soft delete it.
6. Show Deleted Categories.
7. Restore it.
8. Create an expense.
9. Update the expense.
10. Soft delete and restore the expense.
11. Run several reports.
12. Build a Custom Report.
13. Export the report to JSON.
14. Export the report to CSV.
15. Import a small CSV or JSON expense file.
16. Open `logs/finance_tracker.log`.
17. Show that operations were logged.
18. Show the SQLite database.
19. Run `seed.py` again and demonstrate that seed records are skipped instead of duplicated.

---

# Development / Build Plan

The following section documents the sequence in which the project was designed and built.

## Step 1 — Define the problem

The project started from the Expense Tracking exam variant.

The required entities were identified:

```text
Category
Expense
```

Required relationship:

```text
Expense -> Category
```

Required functionality:

```text
CRUD
Validation
Reports
SQLite
CSV/JSON export
Console menus
```

Additional planned features:

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

## Step 2 — Design the architecture

Before implementing all features, the project was separated into layers:

```text
Models
Repositories
Services
CLI
Database
Utilities
```

Reason:

- SQL should not be mixed with menu code;
- validation should not be duplicated;
- business logic should be reusable;
- a future GUI should be able to reuse Services.

Final main flow:

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

## Step 3 — Build the SQLite database

`database/db.py` was created.

Responsibilities:

- define `DB_PATH`;
- create database connections;
- enable foreign keys;
- initialize `categories`;
- initialize `expenses`.

This established SQLite as the primary source of truth.

---

## Step 4 — Create data models

`Category` and `Expense` dataclasses were created.

They provide structured Python objects passed between repositories, services, and CLI code.

This avoids passing unrelated loose values throughout the application.

---

## Step 5 — Build Category Repository

The category repository was implemented first.

Database operations included:

- create;
- read by ID;
- read by name;
- list;
- update;
- soft delete;
- restore;
- list deleted.

This created the first complete persistence layer.

---

## Step 6 — Build Category Service

Business rules were added above the repository:

- name cannot be empty;
- duplicate categories are rejected;
- ID must be valid;
- missing categories produce errors;
- repository calls are hidden from CLI.

Category CRUD could now be used without writing SQL in the menu.

---

## Step 7 — Build Category CLI

A category console menu was added.

Operations:

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

This completed the first end-to-end flow:

```text
CLI -> Service -> Repository -> SQLite
```

---

## Step 8 — Build Expense Repository

The same layered pattern was applied to Expenses.

Repository operations included:

- create;
- get active expense;
- get all active expenses;
- update;
- soft delete;
- restore;
- get deleted expenses.

---

## Step 9 — Build Expense Service

Expense business rules were implemented:

- required expense name;
- positive amount;
- valid date;
- valid category;
- normalized currency;
- date conversion from UI format to database format.

Amounts were stored in cents.

Dates were stored in ISO format.

---

## Step 10 — Build Expense CLI

Expense menu operations were added:

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

The CLI retrieves categories and allows the user to assign a valid category to an expense.

---

## Step 11 — Centralize Validators

Repeated input logic was moved into:

```text
utils/validators.py
```

Reusable functions were created for:

- IDs;
- names;
- descriptions;
- amounts;
- dates;
- currencies;
- numeric selections.

Custom exceptions were introduced:

```text
PreviousField
CancelOperation
```

This created consistent `B` and `X` navigation throughout the application.

---

## Step 12 — Build Shared Console UI

Common display helpers were moved into:

```text
cli/console_ui.py
```

This includes:

- borders;
- centered output;
- centered input;
- shared headers;
- pause/wait behavior.

The result is a consistent console interface.

---

## Step 13 — Build Report Repository

Report SQL was kept focused on raw expense retrieval.

The report repository retrieves expenses by:

- category;
- name;
- date range.

Aggregation was deliberately kept out of SQL where mixed currencies could make direct totals incorrect.

---

## Step 14 — Build Currency Service

Currency conversion was added using Monobank.

Important design decision:

```text
Do not call the API once per expense.
```

Instead:

1. load rates once;
2. cache rates for five minutes;
3. reuse rates;
4. convert through UAH;
5. aggregate converted values in Python.

This made mixed-currency reporting possible.

---

## Step 15 — Build Report Service

The report service combines:

```text
raw expenses + currency rates + calculations
```

The service performs calculations such as:

- max;
- min;
- totals;
- top category;
- average daily spending.

This keeps analytical logic outside both CLI and repository layers.

---

## Step 16 — Build Report CLI

The report menu was added.

The user can provide report-specific parameters such as:

- category;
- name;
- date range;
- target currency.

Results are then formatted and displayed in the console.

---

## Step 17 — Build Custom Report Builder

A Custom Report Builder was added so multiple report sections can be generated together.

The user selects:

```text
number of sections
report types
target currency
```

The generated report is stored in memory as the latest report.

A shortcut automatically selects all sections if the user requests all 11.

---

## Step 18 — Add Report Storage

`services/report_storage.py` stores the last generated custom report.

Purpose:

- report creation and export remain separate;
- the export menu can access the most recent report;
- no database table is needed for temporary report state.

---

## Step 19 — Add JSON and CSV Export

`services/export_service.py` was created.

Features:

- automatic `exports/` directory creation;
- timestamped filenames;
- full JSON export;
- universal CSV export.

The exporter receives a report object and does not need to know how the report was generated.

---

## Step 20 — Add Expense Import

`services/import_service.py` and `cli/import_menu.py` were added.

Import supports:

```text
CSV
JSON
```

Imported expense rows are passed through the existing Expense Service instead of directly inserting into SQLite.

This reuses existing validation and relationship checks.

---

## Step 21 — Add Seed Data

`seed.py` was created to provide a large, useful test dataset.

The script creates:

```text
12 categories
10 expenses per category per month
36 months
4320 expenses
```

A seed marker prevents duplicate seed records when the script is run repeatedly.

---

## Step 22 — Add Logging

`utils/logger.py` was created using Python's `logging` module.

Logging was then connected to:

- `main.py`;
- Category Service;
- Expense Service;
- Import Service;
- Export Service;
- Currency Service.

Reads are intentionally not logged to avoid unnecessary log noise.

---

## Step 23 — Final Integration

The final application flow is:

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

Supporting systems:

```text
SQLite
Monobank API
CSV / JSON
Logging
Seed data
```

---

## 24. Design Decisions

### Why Services?

Services contain business logic and prevent CLI code from directly manipulating the database.

### Why Repositories?

Repositories isolate SQL and make database operations easier to maintain.

### Why store cents?

Integer cents avoid floating-point inaccuracies.

### Why ISO database dates?

`YYYY-MM-DD` is sortable and database-friendly.

### Why soft delete?

Records can be restored and historical data is preserved.

### Why current exchange rates?

The project does not maintain a historical exchange-rate database. Current Monobank rates provide a practical conversion mechanism for reporting.

### Why cache rates?

A report may contain thousands of expenses. Loading currency rates once is significantly more efficient than calling the API for every conversion.

### Why import through Expense Service?

It prevents imported records from bypassing application validation.

### Why log writes but not every read?

Important state-changing actions remain traceable without filling the log with thousands of repetitive read events.

---

## 25. Error Handling

The application handles expected errors close to the operation that can cause them.

Examples:

- invalid IDs;
- invalid dates;
- invalid amounts;
- missing categories;
- missing expenses;
- duplicate category names;
- unsupported currencies;
- missing import files;
- invalid JSON;
- invalid CSV rows;
- Monobank network problems.

Unexpected top-level failures are logged by `main.py` with a traceback.

---

## 26. Current Limitations

1. The application is console-based.
2. Currency conversion uses current rates instead of historical rates.
3. The latest custom report is stored in memory only.
4. Expense import expects referenced categories to exist.
5. SQLite is used as a local single-file database.
6. Seed data is demonstration data and is not intended to represent real financial history.

---

## 27. Future Improvements

Possible future development:

- desktop GUI;
- historical currency-rate storage;
- charts and dashboards;
- budgets;
- recurring expenses;
- user accounts;
- authentication;
- database migrations;
- automated unit tests;
- integration tests;
- configurable currencies;
- advanced import mapping;
- report history stored in SQLite;
- PDF report export.

The current architecture allows these features to be added without replacing the core repository/service design.

---

## 28. Git Workflow

Repository:

```text
https://github.com/johnysilveo/finance_tracker.git
```

Development uses:

```text
main
dev
```

Typical workflow:

```text
develop on dev
        ↓
test
        ↓
merge into main
```

---

## 29. Final Project Checklist

Before submission:

- [ ] `python main.py` starts without errors
- [ ] database initializes automatically
- [ ] Category CRUD works
- [ ] Category soft delete/restore works
- [ ] Expense CRUD works
- [ ] Expense soft delete/restore works
- [ ] validation rejects bad data
- [ ] all report modes execute
- [ ] Custom Report Builder works
- [ ] USD/EUR/UAH conversion works
- [ ] Monobank failure is handled
- [ ] CSV report export works
- [ ] JSON report export works
- [ ] CSV expense import works
- [ ] JSON expense import works
- [ ] invalid import rows are reported
- [ ] `python seed.py` works
- [ ] repeated seed does not duplicate seed data
- [ ] logging file is created
- [ ] CRUD writes appear in logs
- [ ] export/import events appear in logs
- [ ] README matches the final code
- [ ] `.gitignore` excludes runtime/generated files where appropriate
- [ ] final tested version is committed to GitHub

---

## 30. Summary

Finance Tracker is a complete layered Python expense-tracking application built around:

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

The project demonstrates separation of concerns, relational data handling, validation, persistence, external API integration, reporting, file processing, and maintainable application architecture.
