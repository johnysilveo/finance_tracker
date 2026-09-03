from database.db import DB_path
import sqlite3



conn = sqlite3.connect(DB_path)

categories = [
    ("Groceries", "Food and household products"),
    ("Restaurants", "Food and drinks"),
    ("Fuel", "Car gas"),
    ("Hotels", "Staying expenses"),
    ("Entertainment", "Movies, amusement parks, etc."),
    ("Car maintenance", "Oil changes, repairs, and other car-related expenses"),
    ("Shopping", "Leisure shopping expenses"),
    ("Phone/Home Internet", "Home internet and cellular bills"),
    ("Lease/Auto Loan", "Monthly car lease or auto loan payments"),
    ("Rent/Mortgage", "Monthly rent or mortgage expenses"),
    ("Subscriptions", "Subscriptions of all kinds"),
    ("Uncategorized", "Expenses that do not fall under any other category")
]

conn.executemany(
    "INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)",
    categories
)

conn.commit()
conn.close()