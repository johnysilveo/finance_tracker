from database.db import init_db
from cli.main_manu import main_menu
from utils.logger import logger


def main():
    logger.info("Application started")
    try:
        init_db()
        main_menu()
    except Exception:
        logger.exception("Unhandled application error")
        raise
    finally:
        logger.info("Application closed")


if __name__ == "__main__":
    main()