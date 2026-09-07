# Stores the last generated custom report in memory.
last_report: dict | None = None


def save_report(report: dict) -> None:
    global last_report
    last_report = report


def get_last_report() -> dict | None:
    return last_report


def clear_last_report() -> None:
    global last_report
    last_report = None