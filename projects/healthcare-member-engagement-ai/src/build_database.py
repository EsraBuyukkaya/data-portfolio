from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "member_engagement.db"


def main() -> None:
    members = pd.read_csv(DATA_DIR / "synthetic_members.csv")
    events = pd.read_csv(DATA_DIR / "synthetic_events.csv")
    outreach = pd.read_csv(DATA_DIR / "synthetic_outreach.csv")

    with sqlite3.connect(DB_PATH) as conn:
        members.to_sql("members", conn, if_exists="replace", index=False)
        events.to_sql("events", conn, if_exists="replace", index=False)
        outreach.to_sql("outreach", conn, if_exists="replace", index=False)

    print(f"Created SQLite database: {DB_PATH}")


if __name__ == "__main__":
    main()
