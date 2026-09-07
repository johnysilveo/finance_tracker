from services import category_service
from cli.console_ui import border, centered, centered_input, wait_for_enter, show_header
from utils.validators import (get_valid_id,get_valid_name,get_description,get_input,PreviousField,CancelOperation)



def category_menu():
    while True:
        show_header("CATEGORIES")
        print(centered("1. Add category"))
        print(centered("2. Show all categories "))
        print(centered("3. Update category"))
        print(centered("4. Delete category"))
        print(centered("5. Restore category"))
        print(centered("6. Show category details"))
        print(centered("7. Show deleted categories"))
        print(centered("0. Back"))
        print(centered())
        print(border())
        print(centered())
        choice = centered_input("Enter choice")
        print(centered())
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
        elif choice == "6":
            show_category_details()
        elif choice == "7":
            show_deleted_categories()
        else:
            print(centered("INVALID INPUT!!!!!!!!!!!!!!!!!!!!"))

        wait_for_enter()



def add_category():
    show_header("ADD CATEGORY")
    print(border())
    print(centered())
    step = 0
    while step < 2:
        try:
            if step == 0:
                name = get_valid_name("Enter category name")
            elif step == 1:
                description = get_description("Enter category description")
            step += 1
            print(centered())
        except PreviousField:
            print(centered())
            if step == 0:
                print(centered("Add category cancelled"))
                print(centered())
                print(border())
                return
            step -= 1
        except CancelOperation:
            print(centered())
            print(centered("Add category cancelled"))
            print(centered())
            print(border())
            return
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
    show_header("ALL CATEGORIES")
    categories = category_service.get_all_categories()
    if not categories:
        print(centered("No categories found"))
    else:
        for category in categories:
            print(centered(f"Category ID: {category.id}. Name: {category.name}"))
    print(centered())
    print(border())


def update_category():
    show_header("UPDATE CATEGORY")
    categories = category_service.get_all_categories()
    if not categories:
        print(centered("No categories found"))
        print(centered())
        print(border())
        return
    for category in categories:
        print(centered(f"Category ID: {category.id}. Name: {category.name}"))
    print(centered())
    print(border())
    print(centered())
    step = 0
    while step < 3:
        try:
            if step == 0:
                category_id = get_valid_id("Enter category ID",category_service.get_category_by_id)
                category = category_service.get_category_by_id(category_id)
                print(centered())
                print(centered(f"Current name: {category.name}"))
                print(centered(f"Current description: {category.description or 'None'}"))
                print(centered())
            elif step == 1:
                name = get_valid_name(f"Enter category name ENTER for current ({category.name})",category.name)
            elif step == 2:
                description = get_description(f"Enter category description ENTER for current ({category.description or 'None'})",category.description)
            step += 1
            print(centered())
        except PreviousField:
            print(centered())
            if step == 0:
                print(centered("Update category cancelled"))
                print(centered())
                print(border())
                return
            step -= 1
        except CancelOperation:
            print(centered())
            print(centered("Update category cancelled"))
            print(centered())
            print(border())
            return
    try:
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
    show_header("DELETE CATEGORY")
    categories = category_service.get_all_categories()
    if not categories:
        print(centered("No categories found"))
        print(centered())
        print(border())
        return
    for category in categories:
        print(centered(f"Category ID: {category.id}. Name: {category.name}"))
    print(centered())
    print(border())
    print(centered())
    step = 0
    while step < 2:
        try:
            if step == 0:
                category_id = get_valid_id("Enter category ID",category_service.get_category_by_id)
                category = category_service.get_category_by_id(category_id)
                print(centered())
                print(centered(f"Category: {category.name}"))
                print(centered(f"Description: {category.description or 'None'}"))
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
    show_header("RESTORE CATEGORY")
    deleted_categories = category_service.get_deleted_categories()
    if not deleted_categories:
        print(centered("No deleted categories found"))
        print(centered())
        print(border())
        return
    for category in deleted_categories:
        print(centered(f"Category ID: {category.id}. Name: {category.name}"))
    print(centered())
    print(border())
    print(centered())
    while True:
        try:
            category_id = get_valid_id("Enter category ID")
            deleted_category = None
            for category in deleted_categories:
                if category.id == category_id:
                    deleted_category = category
                    break
            if deleted_category is None:
                print(centered("Error: Deleted category not found"))
                print(centered())
                continue
            break
        except (PreviousField,CancelOperation):
            print(centered())
            print(centered("Restoration cancelled"))
            print(centered())
            print(border())
            return
    try:
        category_service.restore_category(category_id)
        print(centered())
        print(centered("Category restored successfully"))
        print(centered())
    except ValueError as e:
        print(centered())
        print(centered(f"Error: {e}"))
        print(centered())
    print(border())


def show_category_details():
    show_header("SHOW CATEGORY DETAILS")
    categories = category_service.get_all_categories()
    if not categories:
        print(centered("No categories found"))
        print(centered())
        print(border())
        return
    for category in categories:
        print(centered(f"Category ID: {category.id}. Name: {category.name}"))
    print(centered())
    print(border())
    print(centered())
    try:
        category_id = get_valid_id("Enter category ID",category_service.get_category_by_id)
        category = category_service.get_category_by_id(category_id)
    except (PreviousField,CancelOperation):
        print(centered())
        print(centered("Show category details cancelled"))
        print(centered())
        print(border())
        return
    except ValueError as e:
        print(centered())
        print(centered(f"Error: {e}"))
        print(centered())
        print(border())
        return
    print(centered())
    print(centered(f"Category ID: {category.id}"))
    print(centered(f"Name: {category.name}"))
    print(centered(f"Description: {category.description or 'None'}"))
    print(centered(f"Created at: {category.created_at}"))
    print(centered(f"Updated at: {category.updated_at}"))
    print(centered())
    print(border())


def show_deleted_categories():
    show_header("SHOW DELETED CATEGORIES")
    deleted_categories = category_service.get_deleted_categories()
    if not deleted_categories:
        print(centered("No deleted categories found"))
    else:
        for category in deleted_categories:
            print(centered(f"Category ID: {category.id}. Name: {category.name}"))
    print(centered())
    print(border())