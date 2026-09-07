from cli.console_ui import border, centered, centered_input, show_header
from cli.category_menu import category_menu
from cli.expense_menu import expense_menu
from cli.report_menu import report_menu
from cli.import_menu import import_menu




def main_menu():
    while True:
        show_header("FINANCE TRACKER")
        print(centered("1. Categories"))
        print(centered("2. Expenses"))
        print(centered("3. Reports/Exports"))
        print(centered("4. Import data"))
        print(centered("0. Exit"))
        print(centered())
        print(border())
        print(centered())
        choice = centered_input("Choose option")
        print(centered())

        if choice == "0":
            break
        elif choice == "1":
            category_menu()
        elif choice == "2":
            expense_menu()
        elif choice == "3":
            report_menu()
        elif choice == "4":
            import_menu()
        else:
            print(centered("FUCKING INVALID!!!!!!!!!!!!!!!!!!!!!!!!!!!!"))
