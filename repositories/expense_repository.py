from database.db import get_connection
from models.expense import Expense



def create_expense(expense: Expense) -> int:
    connection = get_connection()
    try:
        cursor = connection.execute(
            "INSERT INTO expenses ("
            "name, "
            "description, "
            "currency, "
            "category_id, "
            "amount_cents, "
            "date) "
            "VALUES (?,?,?,?,?,?)",
            (
                expense.name,
                expense.description,
                expense.currency,
                expense.category_id,
                expense.amount_cents,
                expense.date
            )
        )
        connection.commit()
        return cursor.lastrowid
    finally:
        connection.close()


def get_expense_by_id(expense_id: int) -> Expense | None:
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            SELECT name, description, currency, category_id, amount_cents, date, id, is_deleted, created_at, updated_at
            FROM expenses 
            WHERE id = ? AND is_deleted = 0 
            """,
            (expense_id, )
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return Expense(
            name=row[0],
            description=row[1],
            currency=row[2],
            category_id=row[3],
            amount_cents=row[4],
            date=row[5],
            id= row[6],
            is_deleted= bool(row[7]),
            created_at=row[8],
            updated_at=row[9]
        )
    finally:
        connection.close()


def get_all_expenses() -> list[Expense]:
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            SELECT name, description, currency, category_id, amount_cents, date, id, is_deleted, created_at, updated_at
            FROM expenses 
            WHERE is_deleted = 0 
            ORDER BY id
            """
        )
        rows = cursor.fetchall()
        expenses = []
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
        connection.close()


def update_expense(expense: Expense) -> bool:
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            UPDATE expenses 
            SET name = ?, description = ?, date = ?, amount_cents = ?, category_id = ?, currency = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND is_deleted = 0
            """,
            (expense.name,
             expense.description,
             expense.date,
             expense.amount_cents,
             expense.category_id,
             expense.currency,
             expense.id,
             )
        )
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def soft_delete_expense(expense_id: int) -> bool:
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            UPDATE expenses
            SET is_deleted = 1,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND is_deleted = 0 
            """,
            (expense_id, )
        )
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def restore_expense(expense_id: int) -> bool:
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            UPDATE expenses
            SET is_deleted = 0,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND is_deleted = 1 
            """,
            (expense_id, )
        )
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def get_deleted_expenses() -> list[Expense]:
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            SELECT name, description, currency, category_id, amount_cents, date, id, is_deleted, created_at, updated_at
            FROM expenses 
            WHERE is_deleted = 1 
            ORDER BY id
            """
        )
        rows = cursor.fetchall()
        expenses = []
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
        connection.close()


def has_active_expenses_by_category(category_id: int) -> bool:
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            SELECT 1
            FROM expenses
            WHERE category_id = ? AND is_deleted = 0
            LIMIT 1
            """,
            (category_id,)
        )
        return cursor.fetchone() is not None
    finally:
        connection.close()
