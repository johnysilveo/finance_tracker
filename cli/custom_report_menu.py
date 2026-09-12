from datetime import datetime
from services import report_service, category_service
from services.report_storage import save_report
from cli.console_ui import border, centered, show_header
from utils.validators import (get_valid_number,get_valid_currency,get_valid_id,get_valid_name,get_valid_date,PreviousField,CancelOperation)


REPORT_OPTIONS = {
    1: "Expenses by category",
    2: "Expenses by name",
    3: "Expenses by date range",
    4: "Maximum expense in period",
    5: "Minimum expense in period",
    6: "Maximum expense by category",
    7: "Minimum expense by category",
    8: "Total by category",
    9: "Totals by all categories",
    10: "Top category",
    11: "Average daily expense",
    12: "Maximum expense for each category",
    13: "Minimum expense for each category"
}


# Displays all report sections that can be included in a custom report.
def show_custom_report_options():
    print(centered("AVAILABLE REPORT SECTIONS"))
    print(centered())
    for option,title in REPORT_OPTIONS.items():
        print(centered(f"{option}. {title}"))
    print(centered())


# Displays active categories before a category ID is requested.
def show_categories():
    categories = category_service.get_all_categories()
    if not categories:
        raise ValueError("No categories found")
    print(centered("AVAILABLE CATEGORIES"))
    print(centered())
    for category in categories:
        print(centered(f"{category.id}. {category.name}"))
    print(centered())


# Converts an Expense object into simple structured data that can later be exported to CSV or JSON.
def expense_to_data(expense) -> dict:
    try:
        category = category_service.get_category_by_id(expense.category_id)
        category_name = category.name
    except ValueError:
        category_name = "Deleted category"
    return {
        "id": expense.id,
        "name": expense.name,
        "category_id": expense.category_id,
        "category": category_name,
        "amount_cents": expense.amount_cents,
        "currency": expense.currency,
        "date": expense.date,
        "description": expense.description
    }


# Gets a valid date range while allowing B to return to the previous date field.
def get_report_date_range() -> tuple[str,str]:
    step = 0
    while step < 2:
        try:
            if step == 0:
                start_date = get_valid_date("Enter start date YYYY-MM-DD")
            elif step == 1:
                end_date = get_valid_date("Enter end date YYYY-MM-DD")
                parsed_start_date = datetime.strptime(start_date,"%Y-%m-%d")
                parsed_end_date = datetime.strptime(end_date,"%Y-%m-%d")
                if parsed_start_date > parsed_end_date:
                    print(centered())
                    print(centered("Error: Start date must be before end date"))
                    print(centered())
                    continue
            step += 1
            print(centered())
        except PreviousField:
            if step == 0:
                raise
            step -= 1
            print(centered())
    return start_date,end_date


# Builds one selected report section using the existing report service functions.
def build_report_section(option: int, target_currency: str) -> dict:
    if option == 1:
        show_categories()
        category_id = get_valid_id("Enter category ID",category_service.get_category_by_id)
        category = category_service.get_category_by_id(category_id)
        expenses = report_service.get_expenses_by_category(category_id)
        data = []
        lines = []
        for expense in expenses:
            data.append(expense_to_data(expense))
            amount = expense.amount_cents / 100
            lines.append(f"{expense.name} - {amount:.2f} {expense.currency}")
        return {
            "title": "Expenses by category",
            "parameters": {"category_id": category_id,"category": category.name},
            "data": data,
            "lines": lines
        }

    elif option == 2:
        name = get_valid_name("Enter expense name")
        expenses = report_service.get_expenses_by_name(name)
        data = []
        lines = []
        for expense in expenses:
            data.append(expense_to_data(expense))
            amount = expense.amount_cents / 100
            lines.append(f"{expense.name} - {amount:.2f} {expense.currency}")
        return {
            "title": "Expenses by name",
            "parameters": {"name": name},
            "data": data,
            "lines": lines
        }

    elif option == 3:
        start_date,end_date = get_report_date_range()
        expenses = report_service.get_expenses_by_date_range(start_date,end_date)
        data = []
        lines = []
        for expense in expenses:
            data.append(expense_to_data(expense))
            amount = expense.amount_cents / 100
            display_date = datetime.strptime(expense.date,"%Y-%m-%d").strftime("%Y-%m-%d")
            lines.append(f"{expense.name} - {amount:.2f} {expense.currency} - {display_date}")
        return {
            "title": "Expenses by date range",
            "parameters": {"start_date": start_date,"end_date": end_date},
            "data": data,
            "lines": lines
        }

    elif option == 4:
        start_date,end_date = get_report_date_range()
        expense = report_service.get_max_expense_in_period(start_date,end_date,target_currency)
        data = expense_to_data(expense)
        amount = expense.amount_cents / 100
        display_date = datetime.strptime(expense.date,"%Y-%m-%d").strftime("%Y-%m-%d")
        return {
            "title": "Maximum expense in period",
            "parameters": {"start_date": start_date,"end_date": end_date,"currency": target_currency},
            "data": data,
            "lines": [f"{expense.name} - {amount:.2f} {expense.currency} - {display_date}"]
        }

    elif option == 5:
        start_date,end_date = get_report_date_range()
        expense = report_service.get_min_expense_in_period(start_date,end_date,target_currency)
        data = expense_to_data(expense)
        amount = expense.amount_cents / 100
        display_date = datetime.strptime(expense.date,"%Y-%m-%d").strftime("%Y-%m-%d")
        return {
            "title": "Minimum expense in period",
            "parameters": {"start_date": start_date,"end_date": end_date,"currency": target_currency},
            "data": data,
            "lines": [f"{expense.name} - {amount:.2f} {expense.currency} - {display_date}"]
        }

    elif option == 6:
        show_categories()
        category_id = get_valid_id("Enter category ID",category_service.get_category_by_id)
        category = category_service.get_category_by_id(category_id)
        expense = report_service.get_max_expense_by_category(category_id,target_currency)
        data = expense_to_data(expense)
        amount = expense.amount_cents / 100
        return {
            "title": "Maximum expense by category",
            "parameters": {"category_id": category_id,"category": category.name,"currency": target_currency},
            "data": data,
            "lines": [f"{expense.name} - {amount:.2f} {expense.currency}"]
        }

    elif option == 7:
        show_categories()
        category_id = get_valid_id("Enter category ID",category_service.get_category_by_id)
        category = category_service.get_category_by_id(category_id)
        expense = report_service.get_min_expense_by_category(category_id,target_currency)
        data = expense_to_data(expense)
        amount = expense.amount_cents / 100
        return {
            "title": "Minimum expense by category",
            "parameters": {"category_id": category_id,"category": category.name,"currency": target_currency},
            "data": data,
            "lines": [f"{expense.name} - {amount:.2f} {expense.currency}"]
        }

    elif option == 8:
        show_categories()
        category_id = get_valid_id("Enter category ID",category_service.get_category_by_id)
        category = category_service.get_category_by_id(category_id)
        total_cents = report_service.get_total_by_category(category_id,target_currency)
        total = total_cents / 100
        return {
            "title": "Total by category",
            "parameters": {"category_id": category_id,"category": category.name,"currency": target_currency},
            "data": {"category_id": category_id,"category": category.name,"total_cents": total_cents,"currency": target_currency},
            "lines": [f"{category.name} - {total:.2f} {target_currency}"]
        }

    elif option == 9:
        totals = report_service.get_totals_by_category(target_currency)
        data = []
        lines = []
        for category_id,total_cents in totals:
            try:
                category = category_service.get_category_by_id(category_id)
                category_name = category.name
            except ValueError:
                category_name = "Deleted category"
            data.append({
                "category_id": category_id,
                "category": category_name,
                "total_cents": total_cents,
                "currency": target_currency
            })
            total = total_cents / 100
            lines.append(f"{category_name} - {total:.2f} {target_currency}")
        return {
            "title": "Totals by all categories",
            "parameters": {"currency": target_currency},
            "data": data,
            "lines": lines
        }

    elif option == 10:
        result = report_service.get_top_category(target_currency)
        if result is None:
            raise ValueError("No top category found")
        category_id,total_cents = result
        try:
            category = category_service.get_category_by_id(category_id)
            category_name = category.name
        except ValueError:
            category_name = "Deleted category"
        total = total_cents / 100
        return {
            "title": "Top category",
            "parameters": {"currency": target_currency},
            "data": {"category_id": category_id,"category": category_name,"total_cents": total_cents,"currency": target_currency},
            "lines": [f"{category_name} - {total:.2f} {target_currency}"]
        }

    elif option == 11:
        average_cents = report_service.get_average_daily_expenses(target_currency)
        average = average_cents / 100
        return {
            "title": "Average daily expense",
            "parameters": {"currency": target_currency},
            "data": {"average_cents": average_cents,"currency": target_currency},
            "lines": [f"Average daily expense - {average:.2f} {target_currency}"]
        }

    elif option == 12:
        results = report_service.get_max_expenses_by_all_categories(target_currency)
        data = []
        lines = []
        for category_id,expense in results:
            category = category_service.get_category_by_id(category_id)
            data.append(expense_to_data(expense))
            amount = expense.amount_cents / 100
            lines.append(f"{category.name}: {expense.name} - {amount:.2f} {expense.currency}")
        return {
            "title": "Maximum expense for each category",
            "parameters": {"currency": target_currency},
            "data": data,
            "lines": lines
        }

    elif option == 13:
        results = report_service.get_min_expenses_by_all_categories(target_currency)
        data = []
        lines = []
        for category_id,expense in results:
            category = category_service.get_category_by_id(category_id)
            data.append(expense_to_data(expense))
            amount = expense.amount_cents / 100
            lines.append(f"{category.name}: {expense.name} - {amount:.2f} {expense.currency}")
        return {
            "title": "Minimum expense for each category",
            "parameters": {"currency": target_currency},
            "data": data,
            "lines": lines
        }

    raise ValueError("Invalid report option")


# Displays the completed custom report in the console.
def show_custom_report(report: dict):
    show_header("CUSTOM REPORT")
    print(centered(f"Report currency: {report['currency']}"))
    print(centered())
    for index,section in enumerate(report["sections"],start=1):
        print(border())
        print(centered())
        print(centered(f"{index}. {section['title']}"))
        print(centered())
        for line in section["lines"]:
            print(centered(line))
        print(centered())
    print(border())


# Lets the user choose report sections, generates them and saves the completed report.
def build_custom_report():
    show_header("BUILD CUSTOM REPORT")
    show_custom_report_options()
    print(border())
    print(centered())
    selected_options = []
    section_count = None
    target_currency = None
    all_sections_selected = False
    step = 0
    while True:
        try:
            if step == 0:
                section_count = get_valid_number("How many report sections 1-13", 1, 13)
                if section_count == len(REPORT_OPTIONS):
                    # If all sections are requested, select every report automatically.
                    selected_options = list(REPORT_OPTIONS.keys())
                    all_sections_selected = True
                    step = section_count + 1
                else:
                    all_sections_selected = False
                    if len(selected_options) > section_count:
                        selected_options = selected_options[:section_count]
                    step = 1
                print(centered())
                continue
            if not all_sections_selected and step <= section_count:
                section_number = step
                option = get_valid_number(f"Choose report section {section_number}", 1, 13)
                option_index = section_number - 1
                if option_index < len(selected_options):
                    selected_options[option_index] = option
                else:
                    selected_options.append(option)
                step += 1
                print(centered())
                continue
            if step == section_count + 1:
                target_currency = get_valid_currency("Enter report currency USD/EUR/UAH")
                step += 1
                print(centered())
                continue
            break
        except PreviousField:
            print(centered())
            if step == 0:
                print(centered("Custom report cancelled"))
                print(centered())
                print(border())
                return
            if all_sections_selected and step == section_count + 1:
                selected_options = []
                all_sections_selected = False
                step = 0
            else:
                step -= 1
        except CancelOperation:
            print(centered())
            print(centered("Custom report cancelled"))
            print(centered())
            print(border())
            return
    sections = []
    section_index = 0
    while section_index < len(selected_options):
        option = selected_options[section_index]
        print(centered())
        print(border())
        print(centered())
        print(centered(f"SECTION {section_index + 1}: {REPORT_OPTIONS[option]}"))
        print(centered())
        try:
            section = build_report_section(option,target_currency)
            if section_index < len(sections):
                sections[section_index] = section
                sections = sections[:section_index + 1]
            else:
                sections.append(section)
            section_index += 1
        except PreviousField:
            print(centered())
            if section_index == 0:
                print(centered("Custom report cancelled"))
                print(centered())
                print(border())
                return
            section_index -= 1
            sections = sections[:section_index]
        except CancelOperation:
            print(centered())
            print(centered("Custom report cancelled"))
            print(centered())
            print(border())
            return
        except (ValueError,ConnectionError) as error:
            print(centered())
            print(centered(f"Error: {error}"))
            print(centered())
    report = {
        "title": "Finance Tracker Custom Report",
        "currency": target_currency,
        "sections": sections
    }
    save_report(report)
    show_custom_report(report)
    print(centered())
    print(centered("Report saved as the last report"))
    print(centered())
    print(border())