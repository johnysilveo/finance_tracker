from services import report_service, category_service
from cli.console_ui import (border,centered,centered_input,wait_for_enter,show_header)
from datetime import datetime
from utils.validators import (get_valid_id,get_valid_name,get_valid_currency,get_valid_date,PreviousField,CancelOperation)




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
        print(centered())
        choice = centered_input("Choose option")
        print(centered())
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
        elif choice == "12":
            print(centered("Custom report is not implemented yet"))
        elif choice == "13":
            print(centered("Export is not implemented yet"))
        else:
            print(centered("INVALID OPTION"))

        wait_for_enter()



def expenses_by_category():
    show_header("EXPENSES BY CATEGORY")
    categories = category_service.get_all_categories()
    if not categories:
        print(centered("No categories found"))
        print(centered())
        print(border())
        return
    # Show available categories before asking for an ID.
    for category in categories:
        print(centered(f"{category.id} - {category.name}"))
    print(centered())
    print(border())
    print(centered())
    try:
        category_id = get_valid_id("Enter category ID",category_service.get_category_by_id)
        print(centered())
    except (PreviousField,CancelOperation):
        print(centered())
        print(centered("Report cancelled"))
        print(centered())
        print(border())
        return
    try:
        expenses = report_service.get_expenses_by_category(category_id)
        if not expenses:
            print(centered("No expenses found"))
            print(centered())
            print(border())
            return
        # No conversion is needed because this report only displays original expenses.
        for expense in expenses:
            amount = expense.amount_cents / 100
            print(centered(f"{expense.id} - {expense.name} - {amount:.2f} {expense.currency}"))
        print(centered())
    except ValueError as error:
        print(centered(f"Error: {error}"))
        print(centered())
    print(border())


def expenses_by_name():
    show_header("EXPENSES BY NAME")
    print(border())
    print(centered())
    try:
        name = get_valid_name("Enter expense name")
        print(centered())
    except (PreviousField,CancelOperation):
        print(centered())
        print(centered("Report cancelled"))
        print(centered())
        print(border())
        return
    try:
        expenses = report_service.get_expenses_by_name(name)
        if not expenses:
            print(centered("No expenses found"))
            print(centered())
            print(border())
            return
        for expense in expenses:
            amount = expense.amount_cents / 100
            print(centered(f"{expense.id} - {expense.name} - {amount:.2f} {expense.currency}"))
            print(centered())
    except ValueError as error:
        print(centered(f"Error: {error}"))
        print(centered())
    print(border())



def expenses_by_date_range():
    show_header("EXPENSES BY DATE RANGE")
    print(border())
    print(centered())
    step = 0
    while step < 2:
        try:
            if step == 0:
                start_date = get_valid_date("Enter start date MM/DD/YYYY")
            elif step == 1:
                end_date = get_valid_date("Enter end date MM/DD/YYYY")
                parsed_start_date = datetime.strptime(start_date,"%m/%d/%Y")
                parsed_end_date = datetime.strptime(end_date,"%m/%d/%Y")
                if parsed_start_date > parsed_end_date:
                    print(centered())
                    print(centered("Error: Start date must be before end date"))
                    print(centered())
                    continue
            step += 1
            print(centered())
        except PreviousField:
            print(centered())
            if step == 0:
                print(centered("Report cancelled"))
                print(centered())
                print(border())
                return
            step -= 1
        except CancelOperation:
            print(centered())
            print(centered("Report cancelled"))
            print(centered())
            print(border())
            return
    try:
        expenses = report_service.get_expenses_by_date_range(start_date,end_date)
        for expense in expenses:
            amount = expense.amount_cents / 100
            # Database stores YYYY-MM-DD, but CLI displays MM/DD/YYYY.
            display_date = datetime.strptime(expense.date,"%Y-%m-%d").strftime("%m/%d/%Y")
            print(centered(f"ID: {expense.id}. {expense.name} - {amount:.2f} {expense.currency} - {display_date}"))
        print(centered())
    except ValueError as error:
        print(centered(f"Error: {error}"))
        print(centered())
    print(border())



def max_expense_in_period():
    show_header("MAX EXPENSE IN PERIOD")
    print(border())
    print(centered())
    step = 0
    while step < 3:
        try:
            if step == 0:
                start_date = get_valid_date("Enter start date MM/DD/YYYY")
            elif step == 1:
                end_date = get_valid_date("Enter end date MM/DD/YYYY")
                parsed_start_date = datetime.strptime(start_date,"%m/%d/%Y")
                parsed_end_date = datetime.strptime(end_date,"%m/%d/%Y")
                if parsed_start_date > parsed_end_date:
                    print(centered())
                    print(centered("Error: Start date must be before end date"))
                    print(centered())
                    continue
            elif step == 2:
                target_currency = get_valid_currency("Enter report currency USD/EUR/UAH")
            step += 1
            print(centered())
        except PreviousField:
            print(centered())
            if step == 0:
                print(centered("Report cancelled"))
                print(centered())
                print(border())
                return
            step -= 1
        except CancelOperation:
            print(centered())
            print(centered("Report cancelled"))
            print(centered())
            print(border())
            return
    try:
        # All expenses are converted before the maximum value is selected.
        expense = report_service.get_max_expense_in_period(start_date,end_date,target_currency)
        amount = expense.amount_cents / 100
        display_date = datetime.strptime(expense.date,"%Y-%m-%d").strftime("%m/%d/%Y")
        print(centered(f"ID: {expense.id}. {expense.name} - {amount:.2f} {expense.currency} - {display_date}"))
        print(centered())
    except (ValueError,ConnectionError) as error:
        print(centered(f"Error: {error}"))
        print(centered())
    print(border())



def min_expense_in_period():
    show_header("MIN EXPENSE IN PERIOD")
    print(border())
    print(centered())
    step = 0
    while step < 3:
        try:
            if step == 0:
                start_date = get_valid_date("Enter start date MM/DD/YYYY")
            elif step == 1:
                end_date = get_valid_date("Enter end date MM/DD/YYYY")
                parsed_start_date = datetime.strptime(start_date,"%m/%d/%Y")
                parsed_end_date = datetime.strptime(end_date,"%m/%d/%Y")
                if parsed_start_date > parsed_end_date:
                    print(centered())
                    print(centered("Error: Start date must be before end date"))
                    print(centered())
                    continue
            elif step == 2:
                target_currency = get_valid_currency("Enter report currency USD/EUR/UAH")
            step += 1
            print(centered())
        except PreviousField:
            print(centered())
            if step == 0:
                print(centered("Report cancelled"))
                print(centered())
                print(border())
                return
            step -= 1
        except CancelOperation:
            print(centered())
            print(centered("Report cancelled"))
            print(centered())
            print(border())
            return
    try:
        # All expenses are converted before the minimum value is selected.
        expense = report_service.get_min_expense_in_period(start_date,end_date,target_currency)
        amount = expense.amount_cents / 100
        display_date = datetime.strptime(expense.date,"%Y-%m-%d").strftime("%m/%d/%Y")
        print(centered(f"ID: {expense.id}. {expense.name} - {amount:.2f} {expense.currency} - {display_date}"))
        print(centered())
    except (ValueError,ConnectionError) as error:
        print(centered(f"Error: {error}"))
        print(centered())
    print(border())



def max_expense_by_category():
    show_header("MAX EXPENSE BY CATEGORY")
    categories = category_service.get_all_categories()
    if not categories:
        print(centered("No categories found"))
        print(centered())
        print(border())
        return
    for category in categories:
        print(centered(f"{category.id} - {category.name}"))
    print(centered())
    print(border())
    print(centered())
    step = 0
    while step < 2:
        try:
            if step == 0:
                category_id = get_valid_id("Enter category ID",category_service.get_category_by_id)
            elif step == 1:
                target_currency = get_valid_currency("Enter report currency USD/EUR/UAH")
            step += 1
            print(centered())
        except PreviousField:
            print(centered())
            if step == 0:
                print(centered("Report cancelled"))
                print(centered())
                print(border())
                return
            step -= 1
        except CancelOperation:
            print(centered())
            print(centered("Report cancelled"))
            print(centered())
            print(border())
            return
    try:
        # Service converts the expenses before comparing their values.
        expense = report_service.get_max_expense_by_category(category_id,target_currency)
        amount = expense.amount_cents / 100
        display_date = datetime.strptime(expense.date,"%Y-%m-%d").strftime("%m/%d/%Y")
        print(centered(f"ID: {expense.id}. {expense.name} - {amount:.2f} {expense.currency} - {display_date}"))
        print(centered())
    except (ValueError,ConnectionError) as error:
        print(centered(f"Error: {error}"))
        print(centered())
    print(border())



def min_expense_by_category():
    show_header("MIN EXPENSE BY CATEGORY")
    categories = category_service.get_all_categories()
    if not categories:
        print(centered("No categories found"))
        print(centered())
        print(border())
        return
    for category in categories:
        print(centered(f"{category.id} - {category.name}"))
    print(centered())
    print(border())
    print(centered())
    step = 0
    while step < 2:
        try:
            if step == 0:
                category_id = get_valid_id("Enter category ID",category_service.get_category_by_id)
            elif step == 1:
                target_currency = get_valid_currency("Enter report currency USD/EUR/UAH")
            step += 1
            print(centered())
        except PreviousField:
            print(centered())
            if step == 0:
                print(centered("Report cancelled"))
                print(centered())
                print(border())
                return
            step -= 1
        except CancelOperation:
            print(centered())
            print(centered("Report cancelled"))
            print(centered())
            print(border())
            return
    try:
        # Service converts the expenses before comparing their values.
        expense = report_service.get_min_expense_by_category(category_id,target_currency)
        amount = expense.amount_cents / 100
        display_date = datetime.strptime(expense.date,"%Y-%m-%d").strftime("%m/%d/%Y")
        print(centered(f"ID: {expense.id}. {expense.name} - {amount:.2f} {expense.currency} - {display_date}"))
        print(centered())
    except (ValueError,ConnectionError) as error:
        print(centered(f"Error: {error}"))
        print(centered())
    print(border())



def total_by_category():
    show_header("TOTAL BY CATEGORY")
    categories = category_service.get_all_categories()
    if not categories:
        print(centered("No categories found"))
        print(centered())
        print(border())
        return
    for category in categories:
        print(centered(f"{category.id} - {category.name}"))
    print(centered())
    print(border())
    print(centered())
    step = 0
    while step < 2:
        try:
            if step == 0:
                category_id = get_valid_id("Enter category ID",category_service.get_category_by_id)
            elif step == 1:
                target_currency = get_valid_currency("Enter report currency USD/EUR/UAH")
            step += 1
            print(centered())
        except PreviousField:
            print(centered())
            if step == 0:
                print(centered("Report cancelled"))
                print(centered())
                print(border())
                return
            step -= 1
        except CancelOperation:
            print(centered())
            print(centered("Report cancelled"))
            print(centered())
            print(border())
            return
    try:
        category = category_service.get_category_by_id(category_id)
        category_name = category.name
        # Service converts every expense before calculating the total.
        total_cents = report_service.get_total_by_category(category_id,target_currency)
        total = total_cents / 100
        print(centered(f"Total for category ID: {category_id}. {category_name} is {total:.2f} {target_currency}"))
        print(centered())
    except (ValueError,ConnectionError) as error:
        print(centered(f"Error: {error}"))
        print(centered())
    print(border())



def totals_by_categories():
    show_header("TOTALS BY ALL CATEGORIES")
    print(border())
    print(centered())
    try:
        target_currency = get_valid_currency("Enter report currency USD/EUR/UAH")
        print(centered())
    except (PreviousField,CancelOperation):
        print(centered())
        print(centered("Report cancelled"))
        print(centered())
        print(border())
        return
    try:
        totals = report_service.get_totals_by_category(target_currency)
        if not totals:
            print(centered("No totals found"))
            print(centered())
            print(border())
            return
        for category_id,total_cents in totals:
            try:
                category = category_service.get_category_by_id(category_id)
                category_name = category.name
            except ValueError:
                # Expenses may reference a category that has been soft deleted.
                category_name = "Deleted category"
            total = total_cents / 100
            print(centered(f"Total for category: {category_name} is {total:.2f} {target_currency}"))
        print(centered())
    except (ValueError,ConnectionError) as error:
        print(centered(f"Error: {error}"))
        print(centered())
    print(border())



def top_category():
    show_header("TOP CATEGORY")
    print(border())
    print(centered())
    try:
        target_currency = get_valid_currency("Enter report currency USD/EUR/UAH")
        print(centered())
    except (PreviousField,CancelOperation):
        print(centered())
        print(centered("Report cancelled"))
        print(centered())
        print(border())
        return
    try:
        # Service returns the category ID and its converted total.
        result = report_service.get_top_category(target_currency)
        if result is None:
            print(centered("No top category found"))
            print(centered())
            print(border())
            return
        category_id,total_cents = result
        try:
            category = category_service.get_category_by_id(category_id)
            category_name = category.name
        except ValueError:
            category_name = "Deleted category"
        total = total_cents / 100
        print(centered(f"Top category: {category_name} - {total:.2f} {target_currency}"))
        print(centered())
    except (ValueError,ConnectionError) as error:
        print(centered(f"Error: {error}"))
        print(centered())
    print(border())



def average_daily_expense():
    show_header("AVERAGE DAILY EXPENSE")
    print(border())
    print(centered())
    try:
        target_currency = get_valid_currency("Enter report currency USD/EUR/UAH")
        print(centered())
    except (PreviousField,CancelOperation):
        print(centered())
        print(centered("Report cancelled"))
        print(centered())
        print(border())
        return
    try:
        average_cents = report_service.get_average_daily_expenses(target_currency)
        average = average_cents / 100
        print(centered(f"Average daily expense: {average:.2f} {target_currency}"))
        print(centered())
    except (ValueError,ConnectionError) as error:
        print(centered(f"Error: {error}"))
        print(centered())
    print(border())