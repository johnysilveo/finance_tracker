import csv
import json
import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from services import expense_service, category_service
from services.currency_service import CURRENCY_CODES
from utils.logger import logger


def find_category_id(row: dict) -> int:
    category_id = str(row.get("category_id","")).strip()
    if category_id:
        if not category_id.isdigit():
            raise ValueError("Category ID must be a number")
        category = category_service.get_category_by_id(int(category_id))
        return category.id
    category_name = str(row.get("category","")).strip()
    if not category_name:
        raise ValueError("Category or category_id is required")
    for category in category_service.get_all_categories():
        if category.name.lower() == category_name.lower():
            return category.id
    raise ValueError(f"Category '{category_name}' not found")


def normalize_import_date(value: str) -> str:
    value = value.strip()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}",value):
        raise ValueError("Date must be in format YYYY-MM-DD")
    try:
        parsed_date = datetime.strptime(value,"%Y-%m-%d")
        return parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date")


def convert_amount_to_cents(value) -> int:
    try:
        amount = Decimal(str(value))
    except InvalidOperation:
        raise ValueError("Amount must be a valid number")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero")
    if amount.as_tuple().exponent < -2:
        raise ValueError("Amount cannot have more than 2 decimal places")
    return int(amount * 100)


def import_expense_row(row: dict) -> int:
    name = str(row.get("name","")).strip()
    if not name:
        raise ValueError("Expense name cannot be empty")
    category_id = find_category_id(row)
    amount_cents = convert_amount_to_cents(row.get("amount",""))
    currency = str(row.get("currency","USD")).strip().upper() or "USD"
    if currency not in CURRENCY_CODES:
        raise ValueError("Currency must be USD, EUR, or UAH")
    date = normalize_import_date(str(row.get("date","")))
    description = str(row.get("description","")).strip() or None
    # Imported rows still pass through the normal service validation.
    return expense_service.create_expense(name=name[:1].upper() + name[1:],amount_cents=amount_cents,date=date,category_id=category_id,description=description,currency=currency)


def import_rows(rows: list[dict]) -> dict:
    imported = 0
    errors = []
    for row_number,row in enumerate(rows,start=1):
        try:
            import_expense_row(row)
            imported += 1
        except (ValueError,TypeError) as error:
            errors.append(f"Row {row_number}: {error}")
            logger.warning(f"Import row failed: row={row_number}, error={error}")
    logger.info(f"Import completed: imported={imported}, failed={len(errors)}")
    return {
        "imported": imported,
        "failed": len(errors),
        "errors": errors
    }


def import_csv(file_path: str) -> dict:
    path = Path(file_path)
    if not path.exists():
        logger.error(f"CSV import failed: file not found: {path}")
        raise FileNotFoundError("File not found")
    if path.suffix.lower() != ".csv":
        logger.error(f"CSV import failed: invalid file type: {path}")
        raise ValueError("File must be CSV")
    with open(path,"r",encoding="utf-8-sig",newline="") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames:
            logger.error(f"CSV import failed: file has no headers: {path}")
            raise ValueError("CSV file has no headers")
        rows = list(reader)
    logger.info(f"CSV import started: file={path}, rows={len(rows)}")
    return import_rows(rows)


def import_json(file_path: str) -> dict:
    path = Path(file_path)
    if not path.exists():
        logger.error(f"JSON import failed: file not found: {path}")
        raise FileNotFoundError("File not found")
    if path.suffix.lower() != ".json":
        logger.error(f"JSON import failed: invalid file type: {path}")
        raise ValueError("File must be JSON")
    try:
        with open(path,"r",encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        logger.error(f"JSON import failed: invalid JSON: {path}")
        raise ValueError("Invalid JSON file")
    # Import expects a list because every object represents one expense.
    if not isinstance(data,list):
        logger.error(f"JSON import failed: root must be a list: {path}")
        raise ValueError("JSON must contain a list of expenses")
    if not all(isinstance(row,dict) for row in data):
        logger.error(f"JSON import failed: invalid expense object: {path}")
        raise ValueError("Every JSON expense must be an object")
    logger.info(f"JSON import started: file={path}, rows={len(data)}")
    return import_rows(data)