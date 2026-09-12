import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from cli.console_ui import centered, centered_input
from services.currency_service import CURRENCY_CODES


class CancelOperation(Exception):
    pass


class PreviousField(Exception):
    pass


def get_input(prompt: str, allow_back: bool=True) -> str:
    value = centered_input(f"{prompt} [B=Back, X=Cancel]").strip()
    if value.lower() == "x":
        raise CancelOperation
    if allow_back and value.lower() == "b":
        raise PreviousField
    return value


def get_valid_id(prompt: str, lookup_function=None, default: int | None=None) -> int:
    while True:
        value = get_input(prompt)
        if not value and default is not None:
            return default
        if not value.isdigit():
            print(centered("Error: ID must be digit"))
            continue
        item_id = int(value)
        if item_id <= 0:
            print(centered("Error: ID must be greater than zero"))
            continue
        try:
            if lookup_function is not None:
                item = lookup_function(item_id)
                if item is None:
                    raise ValueError("ID not found")
            return item_id
        except ValueError as error:
            print(centered(f"Error: {error}"))


def get_valid_name(prompt: str, default: str | None=None) -> str:
    while True:
        name = get_input(prompt)
        if not name and default is not None:
            return default
        if not name:
            print(centered("Error: Name cannot be empty"))
            continue
        return name[:1].upper() + name[1:]


def get_description(prompt: str, default: str | None=None) -> str | None:
    description = get_input(prompt)
    if not description:
        return default
    return description[:1].upper() + description[1:]


def get_valid_amount_cents(prompt: str, default: int | None=None) -> int:
    while True:
        amount_text = get_input(prompt).strip()
        if not amount_text and default is not None:
            return default
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


def get_valid_currency(prompt: str, default: str | None=None) -> str:
    while True:
        currency = get_input(prompt).strip().upper()
        if not currency and default is not None:
            return default.strip().upper()
        if currency not in CURRENCY_CODES:
            print(centered("Error: Currency must be USD, EUR, or UAH"))
            continue
        return currency

def get_valid_date(prompt: str, default: str | None=None) -> str:
    while True:
        date = get_input(prompt)
        if not date and default is not None:
            return default
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}",date):
            print(centered("Error: Date must be in format YYYY-MM-DD"))
            continue
        try:
            datetime.strptime(date,"%Y-%m-%d")
            return date
        except ValueError:
            print(centered("Error: Invalid date"))


def get_valid_date_range(start_prompt: str, end_prompt: str) -> tuple[str,str]:
    while True:
        start_date = get_valid_date(start_prompt)
        end_date = get_valid_date(end_prompt)
        parsed_start_date = datetime.strptime(start_date,"%Y-%m-%d")
        parsed_end_date = datetime.strptime(end_date,"%Y-%m-%d")
        if parsed_start_date <= parsed_end_date:
            return start_date,end_date
        print(centered("Error: Start date must be before end date"))

# def get_valid_date(prompt: str, default: str | None=None) -> str:
#     while True:
#         date = get_input(prompt)
#         if not date and default is not None:
#             return default
#         date = re.sub(r"[.,'\-]+","/",date)
#         parts = date.split("/")
#         if len(parts) != 3:
#             print(centered("Error: Enter month, day and year"))
#             continue
#         month,day,year = parts
#         if not month.isdigit() or not day.isdigit() or not year.isdigit():
#             print(centered("Error: Date must contain numbers"))
#             continue
#         if len(year) <= 2:
#             year = str(2000 + int(year))
#         if len(year) != 4:
#             print(centered("Error: Year must contain 1, 2 or 4 digits"))
#             continue
#         try:
#             parsed_date = datetime(int(year),int(month),int(day))
#             return parsed_date.strftime("%Y-%m-%d")
#         except ValueError:
#             print(centered("Error: Invalid date"))
#
#
# def get_valid_date_range(start_prompt: str, end_prompt: str) -> tuple[str,str]:
#     while True:
#         start_date = get_valid_date(start_prompt)
#         end_date = get_valid_date(end_prompt)
#         parsed_start_date = datetime.strptime(start_date,"%Y-%m-%d")
#         parsed_end_date = datetime.strptime(end_date,"%Y-%m-%d")
#         if parsed_start_date <= parsed_end_date:
#             return start_date,end_date
#         print(centered("Error: Start date must be before end date"))



def get_valid_number(prompt: str, min_value: int, max_value: int) -> int:
    while True:
        value = get_input(prompt)
        if not value.isdigit():
            print(centered("Error: Value must be a number"))
            continue
        number = int(value)
        if number < min_value or number > max_value:
            print(centered(f"Error: Value must be from {min_value} to {max_value}"))
            continue
        return number