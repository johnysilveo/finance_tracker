from datetime import datetime
from decimal import Decimal, InvalidOperation
from cli.console_ui import centered, centered_input
from services.currency_service import CURRENCY_CODES


# Keeps asking until the user enters a valid positive integer ID.
# An optional lookup function can also verify that the object exists.
def get_valid_id(prompt: str, lookup_function=None) -> int:
    while True:
        try:
            item_id = int(centered_input(prompt))
            if item_id <= 0:
                raise ValueError("ID must be greater than zero")
            if lookup_function is not None:
                item = lookup_function(item_id)
                if item is None:
                    raise ValueError("ID not found")
            return item_id
        except ValueError as error:
            print(centered(f"Error: {error}"))


# Keeps asking until the user enters a non-empty name.
# Only the first character is converted to uppercase.
def get_valid_name(prompt: str) -> str:
    while True:
        name = centered_input(prompt).strip()
        if not name:
            print(centered("Error: Name cannot be empty"))
            continue
        return name[:1].upper() + name[1:]


# Description is optional and returns None when the user leaves it empty.
# If entered, only the first character is converted to uppercase.
def get_description(prompt: str) -> str | None:
    description = centered_input(prompt).strip()
    if not description:
        return None
    return description[:1].upper() + description[1:]


# Keeps asking until the user enters a positive amount with maximum two decimal places.
# Returns integer cents so money is never stored as a floating-point number.
def get_valid_amount_cents(prompt: str) -> int:
    while True:
        amount_text = centered_input(prompt).strip()
        try:
            amount = Decimal(amount_text)
            if amount <= 0:
                raise ValueError("Amount must be greater than zero")
            if amount.as_tuple().exponent < -2:
                raise ValueError("Amount cannot have more than 2 decimal places")
            return int(amount * 100)
        except InvalidOperation:
            print(centered("Error: Amount must be a valid number"))
        except ValueError as error:
            print(centered(f"Error: {error}"))


# Keeps asking until the user enters one of the supported currencies.
# Empty input uses USD as the default currency.
def get_valid_currency(prompt: str) -> str:
    while True:
        currency = centered_input(prompt).strip().upper()
        if not currency:
            return "USD"
        if currency not in CURRENCY_CODES:
            print(centered("Error: Currency must be USD, EUR, or UAH"))
            continue
        return currency


# Keeps asking until the user enters a real date.
# Accepts values like 3/5/2026 and normalizes them to 03/05/2026.
def get_valid_date(prompt: str) -> str:
    while True:
        date = centered_input(prompt).strip()
        try:
            parsed_date = datetime.strptime(date,"%m/%d/%Y")
            return parsed_date.strftime("%m/%d/%Y")
        except ValueError:
            print(centered("Error: Date must be in format MM/DD/YYYY"))