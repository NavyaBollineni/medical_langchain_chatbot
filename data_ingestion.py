
import pandas as pd
import json
from pathlib import Path


# Project folder path
BASE_DIR = Path(
    r"C:\Users\SASIDHAR\Desktop\medical_langchain_chatbot\backend"
)

# Excel file path
EXCEL_PATH = Path(
    r"C:\Users\SASIDHAR\Downloads\medical_ai_appointment_chatbot.xlsx"
)

# JSON file will be saved inside the project folder
JSON_PATH = BASE_DIR / "medical_data.json"


def load_data():

    # Read all sheets from Excel
    excel_data = pd.read_excel(
        EXCEL_PATH,
        sheet_name=None
    )

    # Convert all sheets into JSON-compatible data
    json_data = {}

    for sheet_name, dataframe in excel_data.items():

        records = json.loads(
            dataframe.to_json(
                orient="records",
                date_format="iso"
            )
        )

        json_data[sheet_name] = records

    # Save all data into the project folder
    with open(JSON_PATH, "w", encoding="utf-8") as file:

        json.dump(
            json_data,
            file,
            indent=4,
            ensure_ascii=False,
            allow_nan=False
        )

    return json_data


if __name__ == "__main__":
    data = load_data()
