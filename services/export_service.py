import csv
import json
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from utils.logger import logger


EXPORT_DIR = Path(__file__).resolve().parent.parent / "exports"


def prepare_export_directory():
    EXPORT_DIR.mkdir(exist_ok=True)


def create_export_filename(extension: str) -> Path:
    prepare_export_directory()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return EXPORT_DIR / f"finance_report_{timestamp}.{extension}"


def format_cents(value) -> str:
    amount = (Decimal(str(value)) / Decimal("100")).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )
    return f"{amount:.2f}"


def format_export_date(value: str | None) -> str:
    if not value:
        return ""
    try:
        return datetime.strptime(value,"%Y-%m-%d").strftime("%m/%d/%Y")
    except ValueError:
        return value


def clean_parameters(parameters: dict) -> dict:
    cleaned = {}
    for key,value in parameters.items():
        cleaned[key] = value
    return cleaned


def clean_report_item(item: dict) -> dict:
    cleaned = {}
    for key,value in item.items():
        if key == "amount_cents":
            cleaned["amount"] = format_cents(value)
        elif key == "total_cents":
            cleaned["total"] = format_cents(value)
        elif key == "average_cents":
            cleaned["average"] = format_cents(value)
        elif key == "date":
            cleaned["date"] = format_export_date(value)
        else:
            cleaned[key] = value
    return cleaned


def prepare_report_for_json(report: dict) -> dict:
    clean_report = {
        "title": report.get("title","Finance Report"),
        "sections": []
    }
    for section in report.get("sections",[]):
        data = section.get("data",[])
        if isinstance(data,list):
            clean_data = [
                clean_report_item(item) if isinstance(item,dict) else item
                for item in data
            ]
        elif isinstance(data,dict):
            clean_data = clean_report_item(data)
        else:
            clean_data = data
        clean_section = {
            "title": section.get("title",""),
            "parameters": clean_parameters(section.get("parameters",{})),
            "data": clean_data
        }
        clean_report["sections"].append(clean_section)
    return clean_report


def export_report_json(report: dict) -> Path:
    file_path = create_export_filename("json")
    clean_report = prepare_report_for_json(report)
    with open(file_path,"w",encoding="utf-8") as file:
        json.dump(clean_report,file,indent=4,ensure_ascii=False)
    logger.info(f"Report exported to JSON: {file_path}")
    return file_path


def get_csv_row(section_number: int, section_title: str, row_number: int, item: dict) -> list:
    amount = ""
    if "amount_cents" in item:
        amount = format_cents(item["amount_cents"])
    elif "total_cents" in item:
        amount = format_cents(item["total_cents"])
    elif "average_cents" in item:
        amount = format_cents(item["average_cents"])
    return [
        section_number,
        section_title,
        row_number,
        item.get("name",""),
        item.get("category",""),
        amount,
        item.get("currency",""),
        format_export_date(item.get("date")),
        item.get("description","") or ""
    ]


def export_report_csv(report: dict) -> Path:
    file_path = create_export_filename("csv")
    with open(file_path,"w",newline="",encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Section",
            "Report",
            "Row",
            "Name",
            "Category",
            "Amount",
            "Currency",
            "Date",
            "Description"
        ])
        for section_number,section in enumerate(report.get("sections",[]),start=1):
            data = section.get("data",[])
            if isinstance(data,list):
                for row_number,item in enumerate(data,start=1):
                    if isinstance(item,dict):
                        writer.writerow(
                            get_csv_row(
                                section_number,
                                section.get("title",""),
                                row_number,
                                item
                            )
                        )
            elif isinstance(data,dict):
                writer.writerow(
                    get_csv_row(
                        section_number,
                        section.get("title",""),
                        1,
                        data
                    )
                )
    logger.info(f"Report exported to CSV: {file_path}")
    return file_path