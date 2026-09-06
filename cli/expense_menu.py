from services import expense_service, category_service
from cli.console_ui import border, centered, centered_input, wait_for_enter, show_header
from decimal import Decimal, InvalidOperation
from datetime import datetime


def expense_menu():
    while True:
        print(border())
        print(centered())
        print(centered("EXPENSE MENU"))
        print(centered())
        print(centered("1. Add expense"))
        print(centered("2. Show all expenses"))
        print(centered("3. Update expense"))
        print(centered("4. Delete expense"))
        print(centered("5. Restore expense"))
        print(centered("6. Show expense details"))
        print(centered("7. Show deleted expenses"))
        print(centered("0. Back"))
        print(centered())
        print(border())

        choice = centered_input("Choose option")

        if choice == "0":
            break
        elif choice == "1":
            add_expense()
        elif choice == "2":
            show_all_expenses()
        elif choice == "3":
            update_expense()
        elif choice == "4":
            delete_expense()
        elif choice == "5":
            restore_expense()
        elif choice == "6":
            show_expense_details()
        elif choice == "7":
            show_deleted_expenses()
        else:
            print(centered("INVALID!!!!!!!!!!!!!!!!!!!"))

        wait_for_enter()


def add_expense():
    show_header("ADD EXPENSES")
    categories = category_service.get_all_categories()
    if not categories:
        print(centered("No categories found. Create a category first."))
        print(border())
        return
    print(centered("AVAILABLE CATEGORIES"))
    print(centered())
    for category in categories:
        print(centered(f"{category.id}. {category.name}"))
    print(centered())
    name = centered_input("Enter expense name")
    description = centered_input("Enter expense description")
    category_id = centered_input("Enter category ID")
    amount = centered_input("Enter expense amount")
    date = centered_input("Enter expense date MM/DD/YYYY")
    currency = centered_input("Enter currency (default USD)")
    try:
        category_id = int(category_id)
        amount = Decimal(amount)
        if amount.as_tuple().exponent < -2:
            raise ValueError("Amount cannot have more than 2 decimal places")
        amount_cents = int(amount * 100)
        if not description:
            description = None
        if not currency:
            currency = "USD"
        expense_id = expense_service.create_expense(
            name=name,
            amount_cents=amount_cents,
            date=date,
            category_id=category_id,
            description=description,
            currency=currency
        )
        print(centered())
        print(centered(f"Expense created successfully. ID: {expense_id}"))
    except (ValueError, InvalidOperation) as error:
        print(centered())
        print(centered(f"Error: {error}"))
    print(border())


def show_all_expenses():
    show_header("SHOW EXPENSES")
    expenses = expense_service.get_all_expenses()
    if not expenses:
        print(centered("No expenses found."))
    else:
        for expense in expenses:
            amount = expense.amount_cents / 100
            display_date = datetime.strptime(expense.date, "%Y-%m-%d").strftime("%m/%d/%Y")
            try:
                category = category_service.get_category_by_id(expense.category_id)
                category_name = category.name
            except ValueError:
                category_name = "Deleted category"
            print(centered(f"ID: {expense.id}. Name: {expense.name}"))
            print(centered(f"Category: {category_name}"))
            print(centered(f"Amount: {amount:.2f} {expense.currency}"))
            print(centered(f"Date: {display_date}"))
            print(centered(f"Description: {expense.description or '-'}"))
            print(centered())


def update_expense():
    show_header("UPDATE EXPENSES")
    expenses = expense_service.get_all_expenses()
    if not expenses:
        print(centered("No expenses found."))
        return
    for expense in expenses:
        amount = expense.amount_cents / 100
        print(centered(
            f"ID: {expense.id}. Name: {expense.name} - "
            f"Amount: {amount:.2f} {expense.currency}"
        ))
    print(centered())
    try:
        expense_id = int(centered_input("Enter expense ID"))
        existing_expense = expense_service.get_expense_by_id(expense_id)
        print(centered())
        print(centered(f"Current date: {existing_expense.date}"))
        print(centered(
            f"Current description: {existing_expense.description or 'None'}"
        ))
    except ValueError as error:
        print(centered(f"Error: {error}"))
        return
    categories = category_service.get_all_categories()
    print(centered())
    print(centered("AVAILABLE CATEGORIES"))
    print(centered())
    for category in categories:
        print(centered(f"{category.id}. {category.name}"))
    print(centered())
    current_date = datetime.strptime(
        existing_expense.date,
        "%Y-%m-%d"
    ).strftime("%m/%d/%Y")
    name = centered_input(
        f"Enter new name [{existing_expense.name}]"
    )
    description = centered_input(
        f"Enter new description [{existing_expense.description or 'None'}]"
    )
    category_id = centered_input(
        f"Enter new category ID [{existing_expense.category_id}]"
    )
    amount = centered_input(
        f"Enter new amount [{existing_expense.amount_cents / 100:.2f}]"
    )
    date = centered_input(
        f"Enter new date [{current_date}]"
    )
    currency = centered_input(
        f"Enter new currency [{existing_expense.currency}]"
    )
    try:
        if not name:
            name = existing_expense.name
        if not description:
            description = existing_expense.description
        if not category_id:
            category_id = existing_expense.category_id
        else:
            category_id = int(category_id)
        if not amount:
            amount_cents = existing_expense.amount_cents
        else:
            amount = Decimal(amount)
            if amount.as_tuple().exponent < -2:
                raise ValueError(
                    "Amount cannot have more than 2 decimal places"
                )
            amount_cents = int(amount * 100)
        if not date:
            date = current_date
        if not currency:
            currency = existing_expense.currency
        expense_service.update_expense(
            expense_id=expense_id,
            name=name,
            amount_cents=amount_cents,
            date=date,
            category_id=category_id,
            description=description,
            currency=currency
        )
        print(centered())
        print(centered("Expense updated successfully."))
    except (ValueError, InvalidOperation) as error:
        print(centered())
        print(centered(f"Error: {error}"))


def delete_expense():
    show_header("DELETE EXPENSES")
    expenses = expense_service.get_all_expenses()
    if not expenses:
        print(centered("No expenses found."))
        return
    for expense in expenses:
        amount = expense.amount_cents / 100
        print(centered(
            f"ID: {expense.id}. Name: {expense.name} - "
            f"Amount: {amount:.2f} {expense.currency}"
        ))
    print(centered())
    try:
        expense_id = int(centered_input("Enter expense ID"))
        existing_expense = expense_service.get_expense_by_id(expense_id)
        print(centered())
        print(centered(f"Current date: {existing_expense.date}"))
        print(centered(
            f"Current description: {existing_expense.description or 'None'}"
        ))
    except ValueError as error:
        print(centered(f"Error: {error}"))
        return
    try:
        confirmation = centered_input("Are you sure? (y/n)").lower()
        if confirmation != "y":
            print(centered("Delete cancelled"))
            print(centered())
            print(border())
            return
        else:
            expense_service.delete_expense(expense_id)
            print(centered())
            print(centered("Expense deleted successfully"))
            print(centered())
    except ValueError as e:
        print(centered())
        print(centered(f"Error: {e}"))
        print(centered())
    print(border())


def restore_expense():
    show_header("RESTORE EXPENSES")
    expenses = expense_service.get_deleted_expenses()
    if not expenses:
        print(centered("No expenses found."))
        return
    for expense in expenses:
        amount = expense.amount_cents / 100
        print(centered(
            f"ID: {expense.id}. Name: {expense.name} - "
            f"Amount: {amount:.2f} {expense.currency}"
        ))
    print(centered())
    try:
        expense_id = int(centered_input("Enter expense ID"))
        existing_expense = None
        for expense in expenses:
            if expense.id == expense_id:
                existing_expense = expense
                break
        if existing_expense is None:
            raise ValueError("Deleted expense not found.")
        print(centered())
        print(centered(f"Current date: {existing_expense.date}"))
        print(centered(
            f"Current description: {existing_expense.description or 'None'}"
        ))
    except ValueError as error:
        print(centered(f"Error: {error}"))
        return
    try:
        confirmation = centered_input("Are you sure? (y/n)").lower()
        if confirmation != "y":
            print(centered("Restoration cancelled"))
            print(centered())
            print(border())
            return
        else:
            expense_service.restore_expense(expense_id)
            print(centered())
            print(centered("Expense restored successfully"))
            print(centered())
    except ValueError as e:
        print(centered())
        print(centered(f"Error: {e}"))
        print(centered())
    print(border())


def show_expense_details():
    show_header("SHOW EXPENSES DETAILS")
    expenses = expense_service.get_all_expenses()
    if not expenses:
        print(centered("No expenses found."))
        return
    for expense in expenses:
        amount = expense.amount_cents / 100
        print(centered(
            f"ID: {expense.id}. Name: {expense.name} - "
            f"Amount: {amount:.2f} {expense.currency}"
        ))
    print(centered())
    try:
        expense_id = int(centered_input("Enter expense ID"))
        existing_expense = expense_service.get_expense_by_id(expense_id)

    except ValueError as error:
        print(centered(f"Error: {error}"))
        return
    try:
        category = category_service.get_category_by_id(existing_expense.category_id)
        category_name = category.name
    except ValueError:
        category_name = "Deleted category"

    amount = existing_expense.amount_cents / 100
    display_date = datetime.strptime(existing_expense.date, "%Y-%m-%d").strftime("%m/%d/%Y")
    print(centered())
    print(centered(f"ID: {existing_expense.id}"))
    print(centered(f"Name: {existing_expense.name}"))
    print(centered(f"Category: {category_name}"))
    print(centered(f"Amount: {amount:.2f} {existing_expense.currency}"))
    print(centered(f"Date: {display_date}"))
    print(centered(f"Description: {existing_expense.description or 'None'}"))
    print(centered(f"Created at: {existing_expense.created_at}"))
    print(centered(f"Updated at: {existing_expense.updated_at}"))


def show_deleted_expenses():
    show_header("DELETED EXPENSES")
    expenses = expense_service.get_deleted_expenses()
    if not expenses:
        print(centered("No expenses found."))
        return
    for expense in expenses:
        amount = expense.amount_cents / 100
        display_date = datetime.strptime(expense.date, "%Y-%m-%d").strftime("%m/%d/%Y")
        print(centered(
            f"ID: {expense.id}. Name: {expense.name} - "
            f"Amount: {amount:.2f} {expense.currency}"
        ))
        print(centered(f"Date: {display_date}"))
        print(centered(f"Description: {expense.description or 'None'}"))
        print(centered())


expense_menu()