from services import expense_service, category_service
from cli.console_ui import border, centered, centered_input, wait_for_enter, show_header
from datetime import datetime
from utils.validators import (get_valid_id,get_valid_name,get_description,get_valid_amount_cents,get_valid_currency,get_valid_date,get_input,PreviousField,CancelOperation)


def expense_menu():
    while True:
        show_header("EXPENSE MENU")
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
        print(centered())
        choice = centered_input("Choose option")
        print(centered())
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
            print(centered("INVALID INPUT"))
        wait_for_enter()


def add_expense():
    show_header("ADD EXPENSES")
    categories = category_service.get_all_categories()
    if not categories:
        print(centered("No categories found. Create a category first."))
        print(centered())
        print(border())
        return
    print(centered("AVAILABLE CATEGORIES"))
    print(centered())
    for category in categories:
        print(centered(f"{category.id}. {category.name}"))
    print(centered())
    print(border())
    print(centered())
    step = 0
    while step < 6:
        try:
            if step == 0:
                category_id = get_valid_id("Enter category ID",category_service.get_category_by_id)
            elif step == 1:
                name = get_valid_name("Enter expense name")
            elif step == 2:
                description = get_description("Enter expense description")
            elif step == 3:
                amount_cents = get_valid_amount_cents("Enter expense amount")
            elif step == 4:
                currency = get_valid_currency("Enter currency just hit 'ENTER' for (default USD)","USD")
            elif step == 5:
                date = get_valid_date("Enter date YYYY-MM-DD")
            step += 1
            print(centered())
        except PreviousField:
            print(centered())
            if step == 0:
                print(centered("Add expense cancelled"))
                print(centered())
                print(border())
                return
            step -= 1
        except CancelOperation:
            print(centered())
            print(centered("Add expense cancelled"))
            print(centered())
            print(border())
            return
    try:
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
        print(centered())
    except ValueError as error:
        print(centered())
        print(centered(f"Error: {error}"))
        print(centered())
    print(border())


def show_all_expenses():
    show_header("SHOW EXPENSES")
    expenses = expense_service.get_all_expenses()
    if not expenses:
        print(centered("No expenses found."))
    else:
        for expense in expenses:
            amount = expense.amount_cents / 100
            display_date = datetime.strptime(expense.date,"%Y-%m-%d").strftime("%Y-%m-%d")
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
    print(centered())
    print(border())


def update_expense():
    show_header("UPDATE EXPENSES")
    expenses = expense_service.get_all_expenses()
    if not expenses:
        print(centered("No expenses found."))
        print(centered())
        print(border())
        return
    for expense in expenses:
        amount = expense.amount_cents / 100
        print(centered(
            f"ID: {expense.id}. Name: {expense.name} - "
            f"Amount: {amount:.2f} {expense.currency}"
        ))
    print(centered())
    print(border())
    print(centered())
    step = 0
    while step < 7:
        try:
            if step == 0:
                expense_id = get_valid_id("Enter expense ID",expense_service.get_expense_by_id)
                existing_expense = expense_service.get_expense_by_id(expense_id)
                current_date = datetime.strptime(existing_expense.date,"%Y-%m-%d").strftime("%Y-%m-%d")
                print(centered())
                print(centered(f"Current name: {existing_expense.name}"))
                print(centered(f"Current date: {current_date}"))
                print(centered(f"Current amount: {existing_expense.amount_cents / 100:.2f} {existing_expense.currency}"))
                print(centered(f"Current description: {existing_expense.description or 'None'}"))
                print(centered())
                categories = category_service.get_all_categories()
                print(centered("AVAILABLE CATEGORIES"))
                print(centered())
                for category in categories:
                    print(centered(f"{category.id}. {category.name}"))
                print(centered())
            elif step == 1:
                category_id = get_valid_id(f"Enter category ID ENTER for current ({existing_expense.category_id})",category_service.get_category_by_id,existing_expense.category_id)
            elif step == 2:
                name = get_valid_name(f"Enter expense name ENTER for current ({existing_expense.name})",existing_expense.name)
            elif step == 3:
                description = get_description(f"Enter description ENTER for current ({existing_expense.description or 'None'})",existing_expense.description)
            elif step == 4:
                amount_cents = get_valid_amount_cents(f"Enter amount ENTER for current ({existing_expense.amount_cents / 100:.2f})",existing_expense.amount_cents)
            elif step == 5:
                currency = get_valid_currency(f"Enter currency ENTER for current ({existing_expense.currency})",existing_expense.currency)
            elif step == 6:
                date = get_valid_date(f"Enter date ENTER for current ({current_date})",current_date)
            step += 1
            print(centered())
        except PreviousField:
            print(centered())
            if step == 0:
                print(centered("Update expense cancelled"))
                print(centered())
                print(border())
                return
            step -= 1
        except CancelOperation:
            print(centered())
            print(centered("Update expense cancelled"))
            print(centered())
            print(border())
            return
    try:
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
        print(centered())
    except ValueError as error:
        print(centered())
        print(centered(f"Error: {error}"))
        print(centered())
    print(border())


def delete_expense():
    show_header("DELETE EXPENSES")
    expenses = expense_service.get_all_expenses()
    if not expenses:
        print(centered("No expenses found."))
        print(centered())
        print(border())
        return
    for expense in expenses:
        amount = expense.amount_cents / 100
        print(centered(
            f"ID: {expense.id}. Name: {expense.name} - "
            f"Amount: {amount:.2f} {expense.currency}"
        ))
    print(centered())
    print(border())
    print(centered())
    step = 0
    while step < 2:
        try:
            if step == 0:
                expense_id = get_valid_id("Enter expense ID",expense_service.get_expense_by_id)
                existing_expense = expense_service.get_expense_by_id(expense_id)
                current_date = datetime.strptime(existing_expense.date,"%Y-%m-%d").strftime("%Y-%m-%d")
                print(centered())
                print(centered(f"Name: {existing_expense.name}"))
                print(centered(f"Date: {current_date}"))
                print(centered(f"Description: {existing_expense.description or 'None'}"))
                print(centered())
            elif step == 1:
                confirmation = get_input("Are you sure? (y/n)").lower()
                if confirmation == "n":
                    print(centered())
                    print(centered("Delete cancelled"))
                    print(centered())
                    print(border())
                    return
                if confirmation != "y":
                    print(centered("Error: Enter y or n"))
                    print(centered())
                    continue
            step += 1
        except PreviousField:
            print(centered())
            if step == 0:
                print(centered("Delete cancelled"))
                print(centered())
                print(border())
                return
            step -= 1
        except CancelOperation:
            print(centered())
            print(centered("Delete cancelled"))
            print(centered())
            print(border())
            return
    try:
        expense_service.delete_expense(expense_id)
        print(centered())
        print(centered("Expense deleted successfully"))
        print(centered())
    except ValueError as error:
        print(centered())
        print(centered(f"Error: {error}"))
        print(centered())
    print(border())


def restore_expense():
    show_header("RESTORE EXPENSES")
    expenses = expense_service.get_deleted_expenses()
    if not expenses:
        print(centered("No expenses found."))
        print(centered())
        print(border())
        return
    for expense in expenses:
        amount = expense.amount_cents / 100
        print(centered(
            f"ID: {expense.id}. Name: {expense.name} - "
            f"Amount: {amount:.2f} {expense.currency}"
        ))
    print(centered())
    print(border())
    print(centered())
    step = 0
    while step < 2:
        try:
            if step == 0:
                expense_id = get_valid_id("Enter expense ID")
                existing_expense = None
                for expense in expenses:
                    if expense.id == expense_id:
                        existing_expense = expense
                        break
                if existing_expense is None:
                    print(centered("Error: Deleted expense not found"))
                    print(centered())
                    continue
                current_date = datetime.strptime(existing_expense.date,"%Y-%m-%d").strftime("%Y-%m-%d")
                print(centered())
                print(centered(f"Name: {existing_expense.name}"))
                print(centered(f"Date: {current_date}"))
                print(centered(f"Description: {existing_expense.description or 'None'}"))
                print(centered())
            elif step == 1:
                confirmation = get_input("Are you sure? (y/n)").lower()
                if confirmation == "n":
                    print(centered())
                    print(centered("Restoration cancelled"))
                    print(centered())
                    print(border())
                    return
                if confirmation != "y":
                    print(centered("Error: Enter y or n"))
                    print(centered())
                    continue
            step += 1
        except PreviousField:
            print(centered())
            if step == 0:
                print(centered("Restoration cancelled"))
                print(centered())
                print(border())
                return
            step -= 1
        except CancelOperation:
            print(centered())
            print(centered("Restoration cancelled"))
            print(centered())
            print(border())
            return
    try:
        expense_service.restore_expense(expense_id)
        print(centered())
        print(centered("Expense restored successfully"))
        print(centered())
    except ValueError as error:
        print(centered())
        print(centered(f"Error: {error}"))
        print(centered())
    print(border())


def show_expense_details():
    show_header("SHOW EXPENSES DETAILS")
    expenses = expense_service.get_all_expenses()
    if not expenses:
        print(centered("No expenses found."))
        print(centered())
        print(border())
        return
    for expense in expenses:
        amount = expense.amount_cents / 100
        print(centered(
            f"ID: {expense.id}. Name: {expense.name} - "
            f"Amount: {amount:.2f} {expense.currency}"
        ))
    print(centered())
    print(border())
    print(centered())
    try:
        expense_id = get_valid_id("Enter expense ID",expense_service.get_expense_by_id)
        existing_expense = expense_service.get_expense_by_id(expense_id)
    except (PreviousField,CancelOperation):
        print(centered())
        print(centered("Show expense details cancelled"))
        print(centered())
        print(border())
        return
    try:
        category = category_service.get_category_by_id(existing_expense.category_id)
        category_name = category.name
    except ValueError:
        category_name = "Deleted category"
    amount = existing_expense.amount_cents / 100
    display_date = datetime.strptime(existing_expense.date,"%Y-%m-%d").strftime("%Y-%m-%d")
    print(centered())
    print(centered(f"ID: {existing_expense.id}"))
    print(centered(f"Name: {existing_expense.name}"))
    print(centered(f"Category: {category_name}"))
    print(centered(f"Amount: {amount:.2f} {existing_expense.currency}"))
    print(centered(f"Date: {display_date}"))
    print(centered(f"Description: {existing_expense.description or 'None'}"))
    print(centered(f"Created at: {existing_expense.created_at}"))
    print(centered(f"Updated at: {existing_expense.updated_at}"))
    print(centered())
    print(border())


def show_deleted_expenses():
    show_header("DELETED EXPENSES")
    expenses = expense_service.get_deleted_expenses()
    if not expenses:
        print(centered("No expenses found."))
        print(centered())
        print(border())
        return
    for expense in expenses:
        amount = expense.amount_cents / 100
        display_date = datetime.strptime(expense.date,"%Y-%m-%d").strftime("%Y-%m-%d")
        print(centered(
            f"ID: {expense.id}. Name: {expense.name} - "
            f"Amount: {amount:.2f} {expense.currency}"
        ))
        print(centered(f"Date: {display_date}"))
        print(centered(f"Description: {expense.description or 'None'}"))
        print(centered())
    print(border())