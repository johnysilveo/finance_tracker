from services import report_service, category_service
from cli.console_ui import (border,centered,centered_input,wait_for_enter,show_header)
from datetime import datetime



def report_menu():
    while True:
        show_header("REPORTS")

        print(centered("1. Expenses by category"))
        print(centered("2. Expenses by name"))
        print(centered("3. Expenses by date range"))
        print(centered("4. Maximum expense in period"))
        print(centered("5. Minimum expense in period"))
        print(centered("6. Maximum expense by category"))
        print(centered("7. Minimum expense by category"))
        print(centered("8. Total by category"))
        print(centered("9. Totals by all categories"))
        print(centered("10. Top category"))
        print(centered("11. Average daily expense"))
        print(centered("0. Back"))
        print(centered())
        print(border())

        choice = centered_input("Choose option")

        if choice == "0":
            break
        elif choice == "1":
            expenses_by_category()
        elif choice == "2":
            expenses_by_name()
        elif choice == "3":
            expenses_by_date_range()
        elif choice == "4":
            max_expense_in_period()
        elif choice == "5":
            min_expense_in_period()
        elif choice == "6":
            max_expense_by_category()
        elif choice == "7":
            min_expense_by_category()
        elif choice == "8":
            total_by_category()
        elif choice == "9":
            totals_by_categories()
        elif choice == "10":
            top_category()
        elif choice == "11":
            average_daily_expense()
        else:
            print(centered(" FUCK OFFFFFF INVALID!!!!!!!!!!!!!!!!!!!!!"))

        wait_for_enter()


def expenses_by_category():
    show_header("EXPENSES BY CATEGORY")
    categories = category_service.get_all_categories()
    if not categories:
        print(centered("No categories found"))
        return
    for category in categories:
        print(centered(f"{category.id} - {category.name}"))
    print(centered())
    try:
        category_id = int(centered_input("Enter category ID"))
        expenses = report_service.get_expenses_by_category(category_id)
        if not expenses:
            print(centered("No expenses found"))
            return
        for expense in expenses:
            amount = expense.amount_cents / 100
            print(centered(
                f"{expense.id} - {expense.name} - "
                f"{amount:.2f} {expense.currency}"
            ))
    except ValueError as error:
        print(centered(f"Error: {error}"))


def expenses_by_name():
    show_header("EXPENSES BY NAME")
    name = centered_input("Enter expense name")
    try:
        expenses = report_service.get_expenses_by_name(name)
        if not expenses:
            print(centered("No expenses found"))
            return
        for expense in expenses:
            amount = expense.amount_cents / 100
            print(centered(f"{expense.id} - {expense.name} - {amount:.2f} {expense.currency}"))
            print(centered())
    except ValueError as error:
        print(centered(f"Error: {error}"))










