import sqlite3
from pathlib import Path



DB_path = Path(__file__).parent / "finence.db"
conn = sqlite3.connect(DB_path)
conn.execute("PRAGMA foreign_keys=ON")
conn.execute("""
CREATE TABLE IF NOT EXISTS categories(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    is_deleted INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP)
""")
conn.execute(
    " INSERT OR IGNORE INTO categories(name, description) VALUES (?, ?)",
    ("Groceries", "Food and houshold products")
)
conn.execute(
    " INSERT OR IGNORE INTO categories(name, description) VALUES (?, ?)",
    ("Restaurants", "Foods and drinks")
)
conn.execute(
    " INSERT OR IGNORE INTO categories(name, description) VALUES (?, ?)",
    ("Fuel", "Car gas")
)
conn.execute(
    " INSERT OR IGNORE INTO categories(name, description) VALUES (?, ?)",
    ("Hotels", "Staging expenses")
)
conn.execute(
    " INSERT OR IGNORE INTO categories(name, description) VALUES (?, ?)",
    ("Entertainment", "Movies, abusment parks, etc")
)
conn.execute(
    " INSERT OR IGNORE INTO categories(name, description) VALUES (?, ?)",
    ("Car maintenance", "All expenses related to cars as oil change, repairs, etc")
)
conn.execute(
    " INSERT OR IGNORE INTO categories(name, description) VALUES (?, ?)",
    ("Shopping", "All leisure shopping expenses")
)
conn.execute(
    " INSERT OR IGNORE INTO categories(name, description) VALUES (?, ?)",
    ("Phone/Home Internet", "Bills related home internet and cellular expenses")
)
conn.execute(
    " INSERT OR IGNORE INTO categories(name, description) VALUES (?, ?)",
    ("Lease/Auto Loan", "Monthly payments for car")
)
conn.execute(
    " INSERT OR IGNORE INTO categories(name, description) VALUES (?, ?)",
    ("Rent/Mortgage", "Monthly rent or mortgage expenses")
)
conn.execute(
    " INSERT OR IGNORE INTO categories(name, description) VALUES (?, ?)",
    ("Subscriptions", "Subscriptions of all kinds")
)
conn.execute(
    " INSERT OR IGNORE INTO categories(name, description) VALUES (?, ?)",
    ("Uncategorized", "Expenses wich are not falling under any of categories")
)

conn.commit()
conn.close()
