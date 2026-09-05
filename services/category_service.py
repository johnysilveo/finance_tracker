from models.category import Category
from repositories import category_repository


def create_category(name: str, description: str | None = None) -> int:
    name = name.strip()
    if not name:
        raise ValueError('Category name cannot be empty')
    if description is not None:
        description = description.strip()
    existing_category = category_repository.get_category_by_name(name)
    if existing_category is not None:
        raise ValueError('Category already exists')
    category = Category(name=name,
                        description=description)
    return category_repository.create_category(category)

def get_category_by_id(category_id: int) -> Category:
    if category_id <= 0:
        raise ValueError('Category id cannot be negative')
    category = category_repository.get_category_by_id(category_id)
    if category is None:
        raise ValueError('Category does not exist')
    return category

def get_all_categories() -> list[Category]:
    categories = []
    for category in category_repository.get_all_categories():
        categories.append(category)
    return categories

def update_category(category_id: int, name: str, description: str | None = None) -> bool:
    if category_id <= 0:
        raise ValueError('Category id must be greater than zero')
    name = name.strip()
    if not name:
        raise ValueError('Category name cannot be empty')
    if description is not None:
        description = description.strip()

    existing_category = category_repository.get_category_by_id(category_id)
    if existing_category is None:
        raise ValueError('Category does not exist')

    duplicate = category_repository.get_category_by_name(name)
    if duplicate is not None and duplicate.id != category_id:
        raise ValueError('Category already exists')

    updated_category = Category(
        id=category_id,
        name=name,
        description=description,
        is_deleted=existing_category.is_deleted,
        created_at=existing_category.created_at
    )
    return category_repository.update_category(updated_category)

def delete_category(category_id: int) -> None:
    if category_id <= 0:
        raise ValueError('Category id must be greater than zero')

    deleted = category_repository.soft_delete_category(category_id)

    if not deleted:
        raise ValueError('Category does not exist')

def restore_category(category_id: int) -> None:
    if category_id <= 0:
        raise ValueError('Category id must be greater than zero')

    undeleted = category_repository.restore_category(category_id)

    if not undeleted:
        raise ValueError('Category does not exist')


def get_deleted_categories() -> list[Category]:
    deleted_categories = []
    for category in category_repository.get_deleted_categories():
        deleted_categories.append(category)
    return deleted_categories




