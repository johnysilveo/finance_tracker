from cli.console_ui import border, centered, centered_input, show_header
from cli.category_menu import category_menu
from cli.expense_menu import expense_menu



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

        choice = centered_input("Choose option")

        if choice == "0":
            break
        elif choice == "1":
            category_menu()
        elif choice == "2":
            expense_menu()
        elif choice == "3":
            print(centered("not ready"))
        else:
            print(centered("FUCKING INVALID!!!!!!!!!!!!!!!!!!!!!!!!!!!!"))
