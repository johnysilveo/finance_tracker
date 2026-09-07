from services.import_service import import_csv, import_json
from cli.console_ui import border, centered, show_header, wait_for_enter
from utils.validators import get_input, PreviousField, CancelOperation


def show_import_result(result: dict):
    print(centered())
    print(centered("IMPORT RESULT"))
    print(centered())
    print(centered(f"Imported: {result['imported']}"))
    print(centered(f"Failed: {result['failed']}"))
    if result["errors"]:
        print(centered())
        print(centered("ERRORS"))
        print(centered())
        for error in result["errors"]:
            print(centered(error))
    print(centered())
    print(border())


def import_file(import_function):
    try:
        file_path = get_input("Enter full file path").strip().strip('"')
        print(centered())
        result = import_function(file_path)
        show_import_result(result)
    except (PreviousField,CancelOperation):
        print(centered())
        print(centered("Import cancelled"))
        print(centered())
        print(border())
    except (ValueError,FileNotFoundError,OSError) as error:
        print(centered())
        print(centered(f"Error: {error}"))
        print(centered())
        print(border())


def import_menu():
    while True:
        show_header("IMPORT DATA")
        print(centered("1. Import expenses from CSV"))
        print(centered("2. Import expenses from JSON"))
        print(centered("0. Back"))
        print(centered())
        print(border())
        print(centered())
        try:
            choice = get_input("Choose option")
        except (PreviousField,CancelOperation):
            break
        print(centered())
        if choice == "0":
            break
        elif choice == "1":
            import_file(import_csv)
        elif choice == "2":
            import_file(import_json)
        else:
            print(centered("INVALID OPTION"))
        wait_for_enter()