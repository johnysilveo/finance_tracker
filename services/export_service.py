import csv
import json
from datetime import datetime
from pathlib import Path



EXPORT_DIR = Path(__file__).resolve().parent.parent / "exports"


# Creates the export folder if it does not exist.
def prepare_export_directory():
    EXPORT_DIR.mkdir(exist_ok=True)


# Creates a unique filename using the current date and time.
def create_export_filename(extension: str) -> Path:
    prepare_export_directory()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return EXPORT_DIR / f"finance_report_{timestamp}.{extension}"


# Exports the complete report structure to JSON.
def export_report_json(report: dict) -> Path:
    file_path = create_export_filename("json")
    with open(file_path,"w",encoding="utf-8") as file:
        json.dump(report,file,indent=4,ensure_ascii=False)
    return file_path


# Exports the report to a universal CSV format.
# Each report section can contain different data, so structured data is stored as JSON text inside CSV cells.
def export_report_csv(report: dict) -> Path:
    file_path = create_export_filename("csv")
    with open(file_path,"w",newline="",encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "section_number",
            "section_title",
            "parameters",
            "row_number",
            "display_line",
            "data"
        ])
        for section_number,section in enumerate(report["sections"],start=1):
            parameters = json.dumps(section.get("parameters",{}),ensure_ascii=False)
            data = section.get("data",[])
            lines = section.get("lines",[])
            if isinstance(data,list):
                for row_number,item in enumerate(data,start=1):
                    display_line = lines[row_number - 1] if row_number - 1 < len(lines) else ""
                    writer.writerow([
                        section_number,
                        section["title"],
                        parameters,
                        row_number,
                        display_line,
                        json.dumps(item,ensure_ascii=False)
                    ])
            else:
                display_line = lines[0] if lines else ""
                writer.writerow([
                    section_number,
                    section["title"],
                    parameters,
                    1,
                    display_line,
                    json.dumps(data,ensure_ascii=False)
                ])
    return file_path

