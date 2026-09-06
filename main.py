from database.db import init_db
from cli.main_manu import main_menu


def main():
    init_db()
    main_menu()


if __name__ == "__main__":
    main()