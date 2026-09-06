from datetime import datetime
from models.expense import Expense
from repositories import report_repository, category_repository


def get_expenses_by_category(category_id: int) -> list[Expense]:
    if category_id <= 0:
        raise ValueError("Category ID must be greater than zero")
    category = category_repository.get_category_by_id(category_id)
    if category is None:
        raise ValueError("Category not found")
    return report_repository.get_expenses_by_category(category_id)


def get_expenses_by_name(name: str) -> list[Expense]:
    name = name.strip()
    if not name:
        raise ValueError("Name can not be empty")
    expenses = report_repository.get_expenses_by_name(name)
    if not expenses:
        raise ValueError("Expenses not found")
    return expenses


def get_expenses_by_date_range(start_date: str, end_date: str) -> list[Expense]:
    try:
        parsed_start_date = datetime.strptime(start_date, "%m/%d/%Y")
        parsed_end_date = datetime.strptime(end_date, "%m/%d/%Y")
    except ValueError:
        raise ValueError("Dates must be in format MM/DD/YYYY")
    if parsed_start_date > parsed_end_date:
        raise ValueError("Start date must be before end date")
    start_date = parsed_start_date.strftime("%Y-%m-%d")
    end_date = parsed_end_date.strftime("%Y-%m-%d")
    expenses = report_repository.get_expenses_by_date_range(start_date, end_date)
    if not expenses:
        raise ValueError("No expenses found for this date range")
    return expenses


def get_max_expense_in_period(start_date: str, end_date: str) -> Expense | None:
    try:
        parsed_start_date = datetime.strptime(start_date, "%m/%d/%Y")
        parsed_end_date = datetime.strptime(end_date, "%m/%d/%Y")
    except ValueError:
        raise ValueError("Dates must be in format MM/DD/YYYY")
    if parsed_start_date > parsed_end_date:
        raise ValueError("Start date must be before end date")
    start_date = parsed_start_date.strftime("%Y-%m-%d")
    end_date = parsed_end_date.strftime("%Y-%m-%d")
    expenses = report_repository.get_max_expense_in_period(start_date, end_date)
    if not expenses:
        raise ValueError("No expenses found for this date range")
    return expenses


def get_min_expense_in_period(start_date: str, end_date: str) -> Expense | None:
    try:
        parsed_start_date = datetime.strptime(start_date, "%m/%d/%Y")
        parsed_end_date = datetime.strptime(end_date, "%m/%d/%Y")
    except ValueError:
        raise ValueError("Dates must be in format MM/DD/YYYY")
    if parsed_start_date > parsed_end_date:
        raise ValueError("Start date must be before end date")
    start_date = parsed_start_date.strftime("%Y-%m-%d")
    end_date = parsed_end_date.strftime("%Y-%m-%d")
    expenses = report_repository.get_min_expense_in_period(start_date, end_date)
    if not expenses:
        raise ValueError("No expenses found for this date range")
    return expenses


def get_max_expense_by_category(category_id: int) -> Expense:
    if category_id <= 0:
        raise ValueError("Category ID must be greater than zero")
    category = category_repository.get_category_by_id(category_id)
    if category is None:
        raise ValueError("Category not found")
    expense = report_repository.get_max_expense_by_category(category_id)
    if expense is None:
        raise ValueError("Expense not found")
    return expense


def get_min_expense_by_category(category_id: int) -> Expense:
    if category_id <= 0:
        raise ValueError("Category ID must be greater than zero")
    category = category_repository.get_category_by_id(category_id)
    if category is None:
        raise ValueError("Category not found")
    expense = report_repository.get_min_expense_by_category(category_id)
    if expense is None:
        raise ValueError("Expense not found")
    return expense


def get_total_by_category(category_id: int) -> int:
    if category_id <= 0:
        raise ValueError("Category ID must be greater than zero")
    category = category_repository.get_category_by_id(category_id)
    if category is None:
        raise ValueError("Category not found")
    total = report_repository.get_total_by_category(category_id)
    return total


def get_totals_by_category() -> list[tuple[int,int]]:
    totals = report_repository.get_totals_by_category()
    return totals


def get_top_category() -> tuple[int,int] | None:
    return report_repository.get_top_category()


def get_average_daily_expenses() -> float:
    return report_repository.get_average_daily_expenses()










