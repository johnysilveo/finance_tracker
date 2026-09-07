from services import report_service, category_service
from cli.console_ui import (border,centered,centered_input,wait_for_enter,show_header)
from datetime import datetime


# Main menu for all available expense reports.
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
        print(centered("12. Build custom report"))
        print(centered("13. Export last report"))
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
            print(centered("INVALID OPTION"))
        # Stops the menu from immediately redrawing after a report.
        wait_for_enter()


# Shows all active expenses that belong to one selected category.
def expenses_by_category():
    show_header("EXPENSES BY CATEGORY")
    categories = category_service.get_all_categories()
    if not categories:
        print(centered("No categories found"))
        return
    # Show category IDs so the user knows which ID can be selected.
    for category in categories:
        print(centered(f"{category.id} - {category.name}"))
    print(centered())
    try:
        category_id = int(centered_input("Enter category ID"))
        # Service validates the category and returns matching expenses.
        expenses = report_service.get_expenses_by_category(category_id)
        if not expenses:
            print(centered("No expenses found"))
            return
        # These expenses are displayed in their original currencies because no calculation is performed.
        for expense in expenses:
            amount = expense.amount_cents / 100
            print(centered(f"{expense.id} - {expense.name} - {amount:.2f} {expense.currency}"))
    except ValueError as error:
        print(centered(f"Error: {error}"))


# Searches expenses using a full or partial expense name.
def expenses_by_name():
    show_header("EXPENSES BY NAME")
    name = centered_input("Enter expense name")
    try:
        # Service uses repository search and validates an empty search value.
        expenses = report_service.get_expenses_by_name(name)
        if not expenses:
            print(centered("No expenses found"))
            return
        # No currency conversion is required because this report only displays records.
        for expense in expenses:
            amount = expense.amount_cents / 100
            print(centered(f"{expense.id} - {expense.name} - {amount:.2f} {expense.currency}"))
            print(centered())
    except ValueError as error:
        print(centered(f"Error: {error}"))


# Shows all expenses inside a selected date range.
def expenses_by_date_range():
    show_header("EXPENSES BY DATE RANGE")
    start_date = centered_input("Enter start date MM/DD/YYYY")
    end_date = centered_input("Enter end date MM/DD/YYYY")
    try:
        # Service validates both dates and converts them to the database format.
        expenses = report_service.get_expenses_by_date_range(start_date,end_date)
        for expense in expenses:
            amount = expense.amount_cents / 100
            # Database stores YYYY-MM-DD, but CLI displays MM/DD/YYYY.
            display_date = datetime.strptime(expense.date,"%Y-%m-%d").strftime("%m/%d/%Y")
            print(centered(f"ID: {expense.id}. {expense.name} - {amount:.2f} {expense.currency} - {display_date}"))
    except ValueError as error:
        print(centered(f"Error: {error}"))


# Finds the largest expense in a period after all amounts are converted to one report currency.
def max_expense_in_period():
    show_header("MAX EXPENSE IN PERIOD")
    start_date = centered_input("Enter start date MM/DD/YYYY")
    end_date = centered_input("Enter end date MM/DD/YYYY")
    # The user chooses one target currency so expenses with different currencies can be compared correctly.
    target_currency = centered_input("Enter report currency USD/EUR/UAH").strip().upper()
    try:
        # Service converts every expense before finding the maximum.
        expense = report_service.get_max_expense_in_period(start_date,end_date,target_currency)
        amount = expense.amount_cents / 100
        display_date = datetime.strptime(expense.date,"%Y-%m-%d").strftime("%m/%d/%Y")
        print(centered(f"ID: {expense.id}. {expense.name} - {amount:.2f} {expense.currency} - {display_date}"))
    except (ValueError,ConnectionError) as error:
        print(centered(f"Error: {error}"))


# Finds the smallest expense in a period after all amounts are converted to one report currency.
def min_expense_in_period():
    show_header("MIN EXPENSE IN PERIOD")
    start_date = centered_input("Enter start date MM/DD/YYYY")
    end_date = centered_input("Enter end date MM/DD/YYYY")
    # A common currency is required before different monetary values can be compared.
    target_currency = centered_input("Enter report currency USD/EUR/UAH").strip().upper()
    try:
        # Service converts every expense before finding the minimum.
        expense = report_service.get_min_expense_in_period(start_date,end_date,target_currency)
        amount = expense.amount_cents / 100
        display_date = datetime.strptime(expense.date,"%Y-%m-%d").strftime("%m/%d/%Y")
        print(centered(f"ID: {expense.id}. {expense.name} - {amount:.2f} {expense.currency} - {display_date}"))
    except (ValueError,ConnectionError) as error:
        print(centered(f"Error: {error}"))


# Finds the largest expense in one category using the selected report currency.
def max_expense_by_category():
    show_header("MAX EXPENSE BY CATEGORY")
    categories = category_service.get_all_categories()
    if not categories:
        print(centered("No categories found"))
        return
    # Display available categories before asking for an ID.
    for category in categories:
        print(centered(f"{category.id} - {category.name}"))
    print(centered())
    try:
        category_id = int(centered_input("Enter category ID"))
        target_currency = centered_input("Enter report currency USD/EUR/UAH").strip().upper()
        # Service validates the category and compares converted expense amounts.
        expense = report_service.get_max_expense_by_category(category_id,target_currency)
        amount = expense.amount_cents / 100
        display_date = datetime.strptime(expense.date,"%Y-%m-%d").strftime("%m/%d/%Y")
        print(centered(f"ID: {expense.id}. {expense.name} - {amount:.2f} {expense.currency} - {display_date}"))
    except (ValueError,ConnectionError) as error:
        print(centered(f"Error: {error}"))


# Finds the smallest expense in one category using the selected report currency.
def min_expense_by_category():
    show_header("MIN EXPENSE BY CATEGORY")
    categories = category_service.get_all_categories()
    if not categories:
        print(centered("No categories found"))
        return
    # Display available categories before asking for an ID.
    for category in categories:
        print(centered(f"{category.id} - {category.name}"))
    print(centered())
    try:
        category_id = int(centered_input("Enter category ID"))
        target_currency = centered_input("Enter report currency USD/EUR/UAH").strip().upper()
        # Service converts the expenses before comparing their amounts.
        expense = report_service.get_min_expense_by_category(category_id,target_currency)
        amount = expense.amount_cents / 100
        display_date = datetime.strptime(expense.date,"%Y-%m-%d").strftime("%m/%d/%Y")
        print(centered(f"ID: {expense.id}. {expense.name} - {amount:.2f} {expense.currency} - {display_date}"))
    except (ValueError,ConnectionError) as error:
        print(centered(f"Error: {error}"))


# Calculates the total spending of one category in a currency selected by the user.
def total_by_category():
    show_header("TOTAL BY CATEGORY")
    categories = category_service.get_all_categories()
    if not categories:
        print(centered("No categories found"))
        return
    # Show categories so the user can choose a valid category ID.
    for category in categories:
        print(centered(f"{category.id} - {category.name}"))
    print(centered())
    try:
        category_id = int(centered_input("Enter category ID"))
        target_currency = centered_input("Enter report currency USD/EUR/UAH").strip().upper()
        category = category_service.get_category_by_id(category_id)
        category_name = category.name
        # Service converts every expense in the category and then adds the converted values.
        total_cents = report_service.get_total_by_category(category_id,target_currency)
        total = total_cents / 100
        print(centered(f"Total for category ID: {category_id}. {category_name} is {total:.2f} {target_currency}"))
    except (ValueError,ConnectionError) as error:
        print(centered(f"Error: {error}"))


# Calculates totals for every category using the same selected currency.
def totals_by_categories():
    show_header("TOTALS BY ALL CATEGORIES")
    target_currency = centered_input("Enter report currency USD/EUR/UAH").strip().upper()
    try:
        # Service converts all active expenses and groups their totals by category.
        totals = report_service.get_totals_by_category(target_currency)
        if not totals:
            print(centered("No totals found"))
            return
        for category_id,total_cents in totals:
            try:
                category = category_service.get_category_by_id(category_id)
                category_name = category.name
            except ValueError:
                # Expenses may still reference a category that has been soft deleted.
                category_name = "Deleted category"
            total = total_cents / 100
            print(centered(f"Total for category: {category_name} is {total:.2f} {target_currency}"))
    except (ValueError,ConnectionError) as error:
        print(centered(f"Error: {error}"))


# Finds the category with the highest total spending after currency conversion.
def top_category():
    show_header("TOP CATEGORY")
    target_currency = centered_input("Enter report currency USD/EUR/UAH").strip().upper()
    try:
        # Service returns one tuple: category ID and its total amount in the selected currency.
        result = report_service.get_top_category(target_currency)
        if result is None:
            print(centered("No top category found"))
            return
        category_id,total_cents = result
        try:
            category = category_service.get_category_by_id(category_id)
            category_name = category.name
        except ValueError:
            category_name = "Deleted category"
        total = total_cents / 100
        print(centered(f"Top category: {category_name} - {total:.2f} {target_currency}"))
    except (ValueError,ConnectionError) as error:
        print(centered(f"Error: {error}"))


# Calculates the average amount spent per day using one selected report currency.
def average_daily_expense():
    show_header("AVERAGE DAILY EXPENSE")
    target_currency = centered_input("Enter report currency USD/EUR/UAH").strip().upper()
    try:
        # Service converts every expense, creates daily totals, and calculates the arithmetic average.
        average_cents = report_service.get_average_daily_expenses(target_currency)
        average = average_cents / 100
        print(centered(f"Average daily expense: {average:.2f} {target_currency}"))
    except (ValueError,ConnectionError) as error:
        print(centered(f"Error: {error}"))



