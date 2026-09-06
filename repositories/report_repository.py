from database.db import get_connection
from models.expense import Expense



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
            (start_date, end_date)
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


def get_max_expense_in_period(start_date: str, end_date: str) -> Expense | None:
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            SELECT name, description, currency, category_id, amount_cents, date, id, is_deleted, created_at, updated_at
            FROM expenses
            WHERE date BETWEEN ? AND ? and is_deleted = 0
            ORDER BY amount_cents DESC
            LIMIT 1
            """,
            (start_date, end_date)
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
            id=row[6],
            is_deleted=bool(row[7]),
            created_at=row[8],
            updated_at=row[9]
        )

    finally:
        connection.close()


def get_min_expense_in_period(start_date: str, end_date: str) -> Expense | None:
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            SELECT name, description, currency, category_id, amount_cents, date, id, is_deleted, created_at, updated_at
            FROM expenses
            WHERE date BETWEEN ? AND ? and is_deleted = 0
            ORDER BY amount_cents ASC
                LIMIT 1
            """,
            (start_date, end_date)
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
            id=row[6],
            is_deleted=bool(row[7]),
            created_at=row[8],
            updated_at=row[9]
        )

    finally:
        connection.close()


def get_max_expense_by_category(category_id: int) -> Expense | None:

        connection = get_connection()
        try:
            cursor = connection.execute(
                """
                SELECT name,
                       description,
                       currency,
                       category_id,
                       amount_cents, date, id, is_deleted, created_at, updated_at
                FROM expenses
                WHERE category_id = ? AND is_deleted = 0
                ORDER BY amount_cents DESC
                    LIMIT 1
                """,
                (category_id,)
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
                id=row[6],
                is_deleted=bool(row[7]),
                created_at=row[8],
                updated_at=row[9]
            )
        finally:
            connection.close()


def get_min_expense_by_category(category_id: int) -> Expense | None:
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            SELECT name,
                   description,
                   currency,
                   category_id,
                   amount_cents, date, id, is_deleted, created_at, updated_at
            FROM expenses
            WHERE category_id = ? AND is_deleted = 0
            ORDER BY amount_cents ASC
                LIMIT 1
            """,
            (category_id,)
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
            id=row[6],
            is_deleted=bool(row[7]),
            created_at=row[8],
            updated_at=row[9]
        )
    finally:
        connection.close()


def get_total_by_category(category_id: int) -> int:
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            SELECT SUM(amount_cents)
            FROM expenses
            WHERE category_id = ? AND is_deleted = 0
            ORDER BY amount_cents ASC
            """,
            (category_id,)
        )
        row = cursor.fetchone()
        if row[0] is None:
            return 0
        return row[0]
    finally:
        connection.close()


def get_totals_by_category() -> list[tuple[int,int]]:
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            SELECT  category_id, SUM(amount_cents)
            FROM expenses
            WHERE  is_deleted = 0
            GROUP BY category_id
            ORDER BY SUM(amount_cents) DESC
            """,
        )
        rows = cursor.fetchall()
        return rows
    finally:
        connection.close()


def get_top_category() -> tuple[int,int] | None:
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            SELECT category_id, SUM(amount_cents)
            FROM expenses
            WHERE is_deleted = 0
            GROUP BY category_id
            ORDER BY SUM(amount_cents) DESC
            LIMIT 1
            """,
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return row
    finally:
        connection.close()

def get_average_daily_expenses() -> float:
    connection = get_connection()
    cursor = connection.execute(
        """
        SELECT AVG(daily_total)
        FROM (
        SELECT date, SUM(amount_cents) AS daily_total
        FROM expenses
        WHERE is_deleted = 0
        GROUP BY date
             )
        """
    )
    row = cursor.fetchone()
    if row[0] is None:
        return 0.0
    return row[0]


