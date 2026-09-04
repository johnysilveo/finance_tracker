from services import category_service
from cli.console_ui import border, centered, centered_input



def category_menu():
    while True:
        print(border())
        print(centered())
        print(centered("CATEGORIES"))
        print(centered())
        print(centered("1. Add category"))
        print(centered("2. Show all categories "))
        print(centered("3. Update category"))
        print(centered("4. Delete category"))
        print(centered("5. Restore category"))
        print(centered("0. Back"))
        print(centered())
        print(border())
        print()
        choice = centered_input("Enter choice")
        if choice == "0":
            return
        elif choice == "1":
            add_category()
        elif choice == "2":
            show_all_categories()
        elif choice == "3":
            update_category()
        elif choice == "4":
            delete_category()
        elif choice == "5":
            restore_category()
        else:
            print(centered("INVALID INPUT!!!!!!!!!!!!!!!!!!!!"))



def add_category():
    print(border())
    print(centered())
    print(centered("ADD CATEGORY"))
    print(centered())

    name = centered_input("Enter category name")
    description = centered_input("Enter category description (optional)")

    if not description:
        description = None
    try:
        category_id = category_service.create_category(name, description)
        print(centered())
        print(centered(f"Category created successfully. ID: {category_id}"))
        print(centered())
    except ValueError as e:
        print(centered())
        print(centered(f"Error: {e}"))
        print(centered())
    print(border())


def show_all_categories():
    print(border())
    print(centered())
    print(centered("ALL CATEGORIES"))
    print(centered())
    categories = category_service.get_all_categories()
    if not categories:
        print(centered("No categories found"))
    else:
        for category in categories:
            print(centered(f"Category ID: {category.id}. Name: {category.name}"))
    print(centered())
    print(border())


def update_category():
    print(border())
    print(centered())
    print(centered("UPDATE CATEGORY"))
    print(centered())
    try:
        category_id = int(centered_input("Enter category ID"))
        category = category_service.get_category_by_id(category_id)
        print(centered())
        print(centered(f"Current name: {category.name}"))
        print(centered(f"Current description: {category.description or 'None'}"))
        print(centered())

        name = centered_input("Enter category name")
        description = centered_input("Enter category description (optional)")

        if not name:
            name = category.name
        if not description:
            description = category.description
        category_service.update_category(category_id, name, description)
        print(centered())
        print(centered(f"Category updated successfully. ID: {category_id}"))
        print(centered())
    except ValueError as e:
        print(centered())
        print(centered(f"Error: {e}"))
        print(centered())
    print(border())


def delete_category():
    print(border())
    print(centered())
    print(centered("DELETE CATEGORY"))
    print(centered())
    try:
        category_id = int(centered_input("Enter category ID"))
        category = category_service.get_category_by_id(category_id)

        print(centered())
        print(centered(f"Category: {category.name}"))
        print(centered(f"Description: {category.description or 'None'}"))
        print(centered())
        confirmation = centered_input("Are you sure? (y/n)").lower()

        if confirmation != "y":
            print(centered("Delete cancelled"))
            print(centered())
            print(border())
            return

        category_service.delete_category(category_id)
        print(centered())
        print(centered("Category deleted successfully"))
        print(centered())
    except ValueError as e:
        print(centered())
        print(centered(f"Error: {e}"))
        print(centered())
    print(border())


def restore_category():
    print(border())
    print(centered())
    print(centered("RESTORE CATEGORY"))
    print(centered())

    try:
        category_id = int(centered_input("Enter category ID"))

        category_service.restore_category(category_id)
        print(centered())
        print(centered("Category restored successfully"))
        print(centered())
    except ValueError as e:
        print(centered())
        print(centered(f"Error: {e}"))
        print(centered())
    print(border())


