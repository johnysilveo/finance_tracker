from models.expense import Expense
from repositories import expense_repository, category_repository
from datetime import datetime



def create_expense(name: str,
                   amount_cents: int,
                   date: str,
                   category_id: int,
                   description: str | None = None,
                   currency: str = 'USD',
                   ) -> int:
    name = name.strip()
    if not name:
        raise ValueError('Expense name cannot be empty')
    if description is not None:
        description = description.strip()
    try:
        parsed_date = datetime.strptime(date, "%m/%d/%Y")
        date = parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError("Expense date must be in format MM/DD/YYYY")
    if amount_cents <= 0:
        raise ValueError('Amount cents cannot be negative or zero')
    currency = currency.strip().upper()
    if not currency:
        currency = 'USD'
    if category_id <= 0:
        raise ValueError("Category ID must be greater than zero")
    existing_category = category_repository.get_category_by_id(category_id)
    if existing_category is None:
        raise ValueError("Category not found")
    expense = Expense(name=name,
                      amount_cents=amount_cents,
                      date=date,
                      currency=currency,
                      category_id=category_id,
                      description=description,)
    return expense_repository.create_expense(expense)


def get_expense_by_id(expense_id: int) -> Expense:
    if expense_id <= 0:
        raise ValueError('Expense ID must be greater than zero')
    expense = expense_repository.get_expense_by_id(expense_id)
    if expense is None:
        raise ValueError('Expense not found')
    return expense


def get_all_expenses() -> list[Expense]:
    expenses = []
    for expense in expense_repository.get_all_expenses():
        expenses.append(expense)
    return expenses


def update_expense(name: str,
                   expense_id: int,
                   amount_cents: int,
                   date: str,
                   category_id: int,
                   description: str | None = None,
                   currency: str = 'USD',
                   ) -> bool:
    if expense_id <= 0:
        raise ValueError('Expense ID must be greater than zero')
    existing_expense = expense_repository.get_expense_by_id(expense_id)
    if existing_expense is None:
        raise ValueError("Expense not found")
    name = name.strip()
    if not name:
        raise ValueError('Expense name cannot be empty')
    if description is not None:
        description = description.strip()
    try:
        parsed_date = datetime.strptime(date, "%m/%d/%Y")
        date = parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError("Expense date must be in format MM/DD/YYYY")
    if amount_cents <= 0:
        raise ValueError('Amount cents cannot be negative or zero')
    currency = currency.strip().upper()
    if not currency:
        currency = 'USD'
    if category_id <= 0:
        raise ValueError("Category ID must be greater than zero")
    existing_category = category_repository.get_category_by_id(category_id)
    if existing_category is None:
        raise ValueError("Category not found")

    updated_expense = Expense(
                              name=name,
                              id=existing_expense.id,
                              is_deleted=existing_expense.is_deleted,
                              created_at=existing_expense.created_at,
                              date=date,
                              amount_cents=amount_cents,
                              category_id=category_id,
                              currency=currency,
                              description=description,
                              )
    return expense_repository.update_expense(updated_expense)


def delete_expense(expense_id: int) -> None:
    if expense_id <= 0:
        raise ValueError('Expense ID must be greater than zero')
    deleted_expense = expense_repository.soft_delete_expense(expense_id)
    if not deleted_expense:
        raise ValueError('Expense not found')


def restore_expense(expense_id: int) -> None:
    if expense_id <= 0:
        raise ValueError('Expense ID must be greater than zero')
    undeleted_expense = expense_repository.restore_expense(expense_id)
    if not undeleted_expense:
        raise ValueError('Expense not found or already active')

def get_deleted_expenses() -> list[Expense]:
    deleted_expenses = []
    for expense in expense_repository.get_deleted_expenses():
        deleted_expenses.append(expense)
    return deleted_expenses


