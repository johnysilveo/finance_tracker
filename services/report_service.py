from datetime import datetime
from models.expense import Expense
from repositories import report_repository, category_repository, expense_repository
from services.currency_service import CURRENCY_CODES,get_currency_rates,convert_currency


# Creates a temporary Expense with the amount converted to the selected report currency.
# This object is used only for reports and does not change the original database record.

def _convert_expense_for_report(expense: Expense, target_currency: str, rates: list[dict]) -> Expense:
    converted_cents = convert_currency(expense.amount_cents,expense.currency,target_currency,rates)
    return Expense(name=expense.name,date=expense.date,amount_cents=converted_cents,category_id=expense.category_id,description=expense.description,currency=target_currency,id=expense.id,is_deleted=expense.is_deleted,created_at=expense.created_at,updated_at=expense.updated_at)


# Returns all active expenses that belong to one category.

def get_expenses_by_category(category_id: int) -> list[Expense]:

    # Validate the category ID before accessing the database.
    if category_id <= 0:
        raise ValueError("Category ID must be greater than zero")

    # Check that the selected category actually exists and is active.

    category = category_repository.get_category_by_id(category_id)
    if category is None:
        raise ValueError("Category not found")

    # No currency conversion is needed because this report only displays expenses.

    return report_repository.get_expenses_by_category(category_id)


# Searches active expenses by a full or partial expense name.

def get_expenses_by_name(name: str) -> list[Expense]:

    # Remove unnecessary spaces from user input.
    name = name.strip()
    if not name:
        raise ValueError("Name can not be empty")

    # Repository uses SQL LIKE and can return multiple matching expenses.

    expenses = report_repository.get_expenses_by_name(name)
    if not expenses:
        raise ValueError("Expenses not found")

    # No conversion is needed because amounts are only displayed in their original currencies.
    return expenses


# Returns all expenses between two user-selected dates.

def get_expenses_by_date_range(start_date: str, end_date: str) -> list[Expense]:

    # Convert user-friendly MM/DD/YYYY dates into datetime objects for validation.
    try:
        parsed_start_date = datetime.strptime(start_date,"%m/%d/%Y")
        parsed_end_date = datetime.strptime(end_date,"%m/%d/%Y")
    except ValueError:
        raise ValueError("Dates must be in format MM/DD/YYYY")

    # Prevent an invalid period where the start date is after the end date.

    if parsed_start_date > parsed_end_date:
        raise ValueError("Start date must be before end date")

    # Convert dates into YYYY-MM-DD because this is the format stored in SQLite.

    start_date = parsed_start_date.strftime("%Y-%m-%d")
    end_date = parsed_end_date.strftime("%Y-%m-%d")
    expenses = report_repository.get_expenses_by_date_range(start_date,end_date)
    if not expenses:
        raise ValueError("No expenses found for this date range")

    # No conversion is needed because this report only displays original expenses.

    return expenses


# Finds the largest expense in a period after converting all expenses to one selected currency.

def get_max_expense_in_period(start_date: str, end_date: str, target_currency: str) -> Expense:

    # Validate and convert the entered date range.
    try:
        parsed_start_date = datetime.strptime(start_date,"%m/%d/%Y")
        parsed_end_date = datetime.strptime(end_date,"%m/%d/%Y")
    except ValueError:
        raise ValueError("Dates must be in format MM/DD/YYYY")
    if parsed_start_date > parsed_end_date:
        raise ValueError("Start date must be before end date")
    start_date = parsed_start_date.strftime("%Y-%m-%d")
    end_date = parsed_end_date.strftime("%Y-%m-%d")

    # Normalize and validate the currency selected for the report.

    target_currency = target_currency.strip().upper()
    if target_currency not in CURRENCY_CODES:
        raise ValueError("Unsupported report currency")

    # Get every expense in the period because raw SQL MAX cannot correctly compare different currencies.

    expenses = report_repository.get_expenses_by_date_range(start_date,end_date)
    if not expenses:
        raise ValueError("No expenses found for this date range")

    # Download currency rates once and reuse them for every expense.

    rates = get_currency_rates()
    converted_expenses = []
    for expense in expenses:
        converted_expenses.append(_convert_expense_for_report(expense,target_currency,rates))

    # Compare converted amounts and return the largest temporary Expense object.

    return max(converted_expenses,key=lambda expense: expense.amount_cents)


# Finds the smallest expense in a period after converting all expenses to one selected currency.

def get_min_expense_in_period(start_date: str, end_date: str, target_currency: str) -> Expense:

    # Validate and convert the entered date range.

    try:
        parsed_start_date = datetime.strptime(start_date,"%m/%d/%Y")
        parsed_end_date = datetime.strptime(end_date,"%m/%d/%Y")
    except ValueError:
        raise ValueError("Dates must be in format MM/DD/YYYY")
    if parsed_start_date > parsed_end_date:
        raise ValueError("Start date must be before end date")
    start_date = parsed_start_date.strftime("%Y-%m-%d")
    end_date = parsed_end_date.strftime("%Y-%m-%d")

    # Normalize and validate the selected report currency.

    target_currency = target_currency.strip().upper()
    if target_currency not in CURRENCY_CODES:
        raise ValueError("Unsupported report currency")

    # Raw database amounts cannot be compared until all currencies are converted.

    expenses = report_repository.get_expenses_by_date_range(start_date,end_date)
    if not expenses:
        raise ValueError("No expenses found for this date range")

    # Reuse one set of Monobank rates for the entire report.

    rates = get_currency_rates()
    converted_expenses = []
    for expense in expenses:
        converted_expenses.append(_convert_expense_for_report(expense,target_currency,rates))

    # Compare converted values and return the smallest temporary Expense object.

    return min(converted_expenses,key=lambda expense: expense.amount_cents)


# Finds the largest expense inside one category using the selected report currency.

def get_max_expense_by_category(category_id: int, target_currency: str) -> Expense:

    # Validate the category ID and selected currency.
    if category_id <= 0:
        raise ValueError("Category ID must be greater than zero")
    target_currency = target_currency.strip().upper()
    if target_currency not in CURRENCY_CODES:
        raise ValueError("Unsupported report currency")

    # Make sure the category exists before loading its expenses.

    category = category_repository.get_category_by_id(category_id)
    if category is None:
        raise ValueError("Category not found")

    # Load every expense because MAX must be calculated after currency conversion.

    expenses = report_repository.get_expenses_by_category(category_id)
    if not expenses:
        raise ValueError("Expense not found")
    rates = get_currency_rates()
    converted_expenses = []
    for expense in expenses:
        converted_expenses.append(_convert_expense_for_report(expense,target_currency,rates))

    # Return the expense with the largest converted amount.

    return max(converted_expenses,key=lambda expense: expense.amount_cents)


# Finds the smallest expense inside one category using the selected report currency.

def get_min_expense_by_category(category_id: int, target_currency: str) -> Expense:

    # Validate the category ID and selected currency.

    if category_id <= 0:
        raise ValueError("Category ID must be greater than zero")
    target_currency = target_currency.strip().upper()
    if target_currency not in CURRENCY_CODES:
        raise ValueError("Unsupported report currency")

    # Make sure the category exists before loading its expenses.

    category = category_repository.get_category_by_id(category_id)
    if category is None:
        raise ValueError("Category not found")

    # Load every expense because MIN must be calculated after currency conversion.

    expenses = report_repository.get_expenses_by_category(category_id)
    if not expenses:
        raise ValueError("Expense not found")
    rates = get_currency_rates()
    converted_expenses = []
    for expense in expenses:
        converted_expenses.append(_convert_expense_for_report(expense,target_currency,rates))

    # Return the expense with the smallest converted amount.

    return min(converted_expenses,key=lambda expense: expense.amount_cents)


# Calculates the total spending for one category in the selected report currency.

def get_total_by_category(category_id: int, target_currency: str) -> int:

    # Validate the category ID and selected report currency.
    if category_id <= 0:
        raise ValueError("Category ID must be greater than zero")
    target_currency = target_currency.strip().upper()
    if target_currency not in CURRENCY_CODES:
        raise ValueError("Unsupported report currency")

    # Check that the selected category exists.

    category = category_repository.get_category_by_id(category_id)
    if category is None:
        raise ValueError("Category not found")

    # Load original expenses instead of using SQL SUM because currencies may be different.

    expenses = report_repository.get_expenses_by_category(category_id)
    if not expenses:
        return 0
    # Get rates once and reuse them for all conversions.

    rates = get_currency_rates()
    total_cents = 0
    for expense in expenses:
        converted_cents = convert_currency(expense.amount_cents,expense.currency,target_currency,rates)
        total_cents += converted_cents

    # Return the final amount in cents to preserve money precision.
    return total_cents


# Calculates totals for every category after converting all expenses to one selected currency.

def get_totals_by_category(target_currency: str) -> list[tuple[int,int]]:

    # Normalize and validate the currency used for the whole report.

    target_currency = target_currency.strip().upper()
    if target_currency not in CURRENCY_CODES:
        raise ValueError("Unsupported report currency")
    # Load all active expenses only once.
    expenses = expense_repository.get_all_expenses()
    if not expenses:
        return []
    # Reuse one set of exchange rates for the entire calculation.

    rates = get_currency_rates()
    totals = {}
    for expense in expenses:
        converted_cents = convert_currency(expense.amount_cents,expense.currency,target_currency,rates)
        if expense.category_id not in totals:
            totals[expense.category_id] = 0
        totals[expense.category_id] += converted_cents

    # Convert the dictionary into tuples and sort categories from highest total to lowest.

    result = list(totals.items())
    result.sort(key=lambda item: item[1],reverse=True)
    return result


# Returns the category with the highest total spending in the selected currency.

def get_top_category(target_currency: str) -> tuple[int,int] | None:

    # Reuse the totals report because it already converts and sorts every category correctly.

    totals = get_totals_by_category(target_currency)
    if not totals:
        return None
    # The first tuple contains the category with the largest converted total.
    return totals[0]


# Calculates the average amount spent per active spending day in the selected currency.

def get_average_daily_expenses(target_currency: str) -> float:

    # Normalize and validate the currency selected for the report.

    target_currency = target_currency.strip().upper()
    if target_currency not in CURRENCY_CODES:
        raise ValueError("Unsupported report currency")

    # Load all active expenses because daily totals must be rebuilt after currency conversion.

    expenses = expense_repository.get_all_expenses()
    if not expenses:
        return 0.0
    # Get Monobank rates once for all expense conversions.
    rates = get_currency_rates()
    daily_totals = {}
    for expense in expenses:
        converted_cents = convert_currency(expense.amount_cents,expense.currency,target_currency,rates)
        if expense.date not in daily_totals:
            daily_totals[expense.date] = 0
        daily_totals[expense.date] += converted_cents
    # Average only the days that contain at least one expense, matching the original SQL report logic.
    total_cents = sum(daily_totals.values())
    average_cents = total_cents / len(daily_totals)
    return average_cents


