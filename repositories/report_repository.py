from database.db import get_connection
from models.expense import Expense


# Returns all active expenses that belong to one category.
# Repository only reads raw database data and does not perform business calculations.
def get_expenses_by_category(category_id: int) -> list[Expense]:
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            SELECT name, description, currency, category_id, amount_cents, date, id, is_deleted, created_at, updated_at
            FROM expenses
            WHERE category_id = ? AND is_deleted = 0
            ORDER BY date
            """,
            (category_id,)
        )
        rows = cursor.fetchall()
        expenses = []
        # Convert every database row into an Expense model object.
        for row in rows:
            expenses.append(Expense(
                name=row[0],
                description=row[1],
                currency=row[2],
                category_id=row[3],
                amount_cents=row[4],
                date=row[5],
                id=row[6],
                is_deleted=bool(row[7]),
                created_at=row[8],
                updated_at=row[9]
            ))
        return expenses
    finally:
        # Always close the database connection even if an error occurs.
        connection.close()


# Searches active expenses by a full or partial name using SQL LIKE.
def get_expenses_by_name(name: str) -> list[Expense]:
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            SELECT name, description, currency, category_id, amount_cents, date, id, is_deleted, created_at, updated_at
            FROM expenses
            WHERE name LIKE ? AND is_deleted = 0
            ORDER BY date
            """,
            (f"%{name}%",)
        )
        rows = cursor.fetchall()
        expenses = []
        # Convert every matching database row into an Expense model object.
        for row in rows:
            expenses.append(Expense(
                name=row[0],
                description=row[1],
                currency=row[2],
                category_id=row[3],
                amount_cents=row[4],
                date=row[5],
                id=row[6],
                is_deleted=bool(row[7]),
                created_at=row[8],
                updated_at=row[9]
            ))
        return expenses
    finally:
        # Connection must always be closed after the query finishes.
        connection.close()


# Returns all active expenses between two dates stored in YYYY-MM-DD format.
def get_expenses_by_date_range(start_date: str, end_date: str) -> list[Expense]:
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            SELECT name, description, currency, category_id, amount_cents, date, id, is_deleted, created_at, updated_at
            FROM expenses
            WHERE date BETWEEN ? AND ? AND is_deleted = 0
            ORDER BY date
            """,
            (start_date,end_date)
        )
        rows = cursor.fetchall()
        expenses = []
        # Convert every expense in the selected period into an Expense model object.
        for row in rows:
            expenses.append(Expense(
                name=row[0],
                description=row[1],
                currency=row[2],
                category_id=row[3],
                amount_cents=row[4],
                date=row[5],
                id=row[6],
                is_deleted=bool(row[7]),
                created_at=row[8],
                updated_at=row[9]
            ))
        return expenses
    finally:
        # Always release the SQLite connection.
        connection.close()

