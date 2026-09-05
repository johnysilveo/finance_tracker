from dataclasses import dataclass


@dataclass
class Expense:
    name: str
    date: str
    amount_cents: int
    category_id: int

    currency: str = "USD"
    description: str | None = None
    id: int | None = None
    is_deleted: bool = False
    created_at: str | None = None
    updated_at: str | None = None







# CREATE TABLE IF NOT EXISTS expenses (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
# category_id INTEGER NOT NULL REFERENCES categories(id),
# name TEXT NOT NULL,
# currency TEXT NOT NULL DEFAULT 'USD',
# amount_cents INTEGER NOT NULL CHECK(amount_cents > 0),
# date TEXT NOT NULL,
# created_at TEXT DEFAULT CURRENT_TIMESTAMP,
# updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
# is_deleted INTEGER DEFAULT 0,
# description TEXT)