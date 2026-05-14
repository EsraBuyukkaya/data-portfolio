from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "launch_command_center.db"


def main() -> None:
    tables = {
        "customers": "customers.csv",
        "launches": "launches.csv",
        "agent_calls": "agent_calls.csv",
        "blockers": "blockers.csv",
        "bank_marketing_contacts": "bank_marketing_contacts.csv",
    }

    with sqlite3.connect(DB_PATH) as conn:
        for table_name, file_name in tables.items():
            path = DATA_DIR / file_name
            if not path.exists():
                continue
            df = pd.read_csv(path)
            df.to_sql(table_name, conn, if_exists="replace", index=False)

    print(f"Created SQLite database: {DB_PATH}")


if __name__ == "__main__":
    main()
