from database.db import get_connection
from models.category import Category


def create_category(category: Category) -> int:
    connection = get_connection()
    try:
        cursor = connection.execute(
            "INSERT INTO categories (name, description) VALUES (?, ?)",
            (
                category.name,
             category.description
            )
        )
        connection.commit()
        return cursor.lastrowid
    finally:
        connection.close()

def get_category_by_id(category_id: int) -> Category | None:
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            SELECT id, name, description, is_deleted, created_at, updated_at
            FROM categories
            WHERE id = ? AND is_deleted = 0
            """,
            (category_id,)
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return Category(
            id=row[0],
            name=row[1],
            description=row[2],
            is_deleted=bool(row[3]),
            created_at=row[4],
            updated_at=row[5]
        )
    finally:
        connection.close()

def get_all_categories() -> list[Category]:
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            SELECT id, name, description, is_deleted, created_at, updated_at
            FROM categories
            WHERE is_deleted = 0
            ORDER BY id
            """
        )
        rows = cursor.fetchall()
        categories = []
        for row in rows:
            category = Category(
                id=row[0],
                name=row[1],
                description=row[2],
                is_deleted=bool(row[3]),
                created_at=row[4],
                updated_at=row[5],
            )
            categories.append(category)
        return categories
    finally:
        connection.close()

def update_category(category: Category) -> bool:
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            UPDATE categories
            SET name = ?, description = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND is_deleted = 0
            """,
            (category.name,
             category.description,
             category.id)
        )
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()

def soft_delete_category(category_id: int) -> bool:
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            UPDATE categories
            SET is_deleted = 1,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND is_deleted = 0
            """,
            (category_id,)
        )
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()

def restore_category(category_id: int) -> bool:
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            UPDATE categories
            SET is_deleted = 0,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND is_deleted = 1
            """,
            (category_id,)
        )
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()

def get_category_by_name(name:str) -> Category | None:
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            SELECT id, name, description, is_deleted, created_at, updated_at
            FROM categories
            WHERE name = ?""",
            (name,)
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return Category(
            id=row[0],
            name=row[1],
            description=row[2],
            is_deleted=bool(row[3]),
            created_at=row[4],
            updated_at=row[5]
        )
    finally:
        connection.close()


def get_deleted_categories() -> list[Category]:
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            SELECT id, name, description, is_deleted, created_at, updated_at
            FROM categories
            WHERE is_deleted = 1
            ORDER BY id
            """
        )
        rows = cursor.fetchall()
        deleted_categories = []
        for row in rows:
            category = Category(
                id=row[0],
                name=row[1],
                description=row[2],
                is_deleted=bool(row[3]),
                created_at=row[4],
                updated_at=row[5]
            )
            deleted_categories.append(category)
        return deleted_categories
    finally:
        connection.close()
