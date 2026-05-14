from __future__ import annotations

import urllib.request
import zipfile
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
SOURCE_DIR = DATA_DIR / "source"
ZIP_PATH = SOURCE_DIR / "bank_marketing.zip"
RAW_CSV_PATH = SOURCE_DIR / "bank" / "bank-full.csv"
NESTED_BANK_ZIP = SOURCE_DIR / "bank.zip"
PREPARED_CSV_PATH = DATA_DIR / "bank_marketing_contacts.csv"
DATA_URL = "https://archive.ics.uci.edu/static/public/222/bank+marketing.zip"


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    if not ZIP_PATH.exists():
        print("Downloading UCI Bank Marketing dataset...")
        urllib.request.urlretrieve(DATA_URL, ZIP_PATH)

    if not RAW_CSV_PATH.exists():
        print("Extracting dataset...")
        with zipfile.ZipFile(ZIP_PATH, "r") as archive:
            archive.extractall(SOURCE_DIR)

    if not RAW_CSV_PATH.exists() and NESTED_BANK_ZIP.exists():
        print("Extracting nested bank.zip...")
        with zipfile.ZipFile(NESTED_BANK_ZIP, "r") as archive:
            archive.extractall(SOURCE_DIR / "bank")

    df = pd.read_csv(RAW_CSV_PATH, sep=";")
    prepared = df.rename(
        columns={
            "y": "converted",
            "duration": "call_duration_seconds",
            "campaign": "campaign_contacts",
            "pdays": "days_since_previous_contact",
            "previous": "previous_contacts",
            "poutcome": "previous_outcome",
        }
    ).copy()

    prepared.insert(0, "contact_id", [f"BM{i:05d}" for i in range(1, len(prepared) + 1)])
    prepared["converted_flag"] = prepared["converted"].map({"yes": 1, "no": 0})
    prepared["customer_segment"] = prepared["job"].fillna("unknown") + " / " + prepared["education"].fillna("unknown")

    keep_columns = [
        "contact_id",
        "age",
        "job",
        "marital",
        "education",
        "balance",
        "housing",
        "loan",
        "contact",
        "day",
        "month",
        "call_duration_seconds",
        "campaign_contacts",
        "days_since_previous_contact",
        "previous_contacts",
        "previous_outcome",
        "customer_segment",
        "converted",
        "converted_flag",
    ]
    prepared[keep_columns].to_csv(PREPARED_CSV_PATH, index=False)
    print(f"Prepared real customer-contact data: {PREPARED_CSV_PATH}")
    print(f"Rows: {len(prepared):,}")


if __name__ == "__main__":
    main()
