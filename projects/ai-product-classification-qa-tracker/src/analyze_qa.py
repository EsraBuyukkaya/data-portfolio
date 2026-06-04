from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sample_product_evaluations.csv"
OUTPUT_DIR = ROOT / "outputs"
LOW_CONFIDENCE_THRESHOLD = 0.70


def load_rows() -> list[dict[str, str]]:
    with DATA_PATH.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def category_match(row: dict[str, str]) -> str:
    approved = row["reviewer_approved_category"].strip()
    if not approved:
        return "Pending Review"
    return "Match" if row["ai_predicted_category"] == approved else "Mismatch"


def priority(row: dict[str, str]) -> str:
    confidence = float(row["ai_confidence"])
    match = category_match(row)
    if not row["reviewer_approved_category"].strip() or row["review_status"] == "Needs Research":
        return "High"
    if match == "Mismatch" or confidence < LOW_CONFIDENCE_THRESHOLD:
        return "High"
    if confidence < 0.85 or row["error_reason"].strip():
        return "Medium"
    return "Normal"


def build_summary(rows: list[dict[str, str]]) -> dict:
    reviewed = [row for row in rows if row["review_status"] == "Reviewed"]
    matches = [row for row in reviewed if category_match(row) == "Match"]
    return {
        "total_records": len(rows),
        "reviewed_records": len(reviewed),
        "review_completion_rate": round(len(reviewed) / len(rows), 3),
        "reviewed_category_agreement_rate": round(len(matches) / len(reviewed), 3),
        "category_mismatches": sum(category_match(row) == "Mismatch" for row in rows),
        "low_confidence_records": sum(
            float(row["ai_confidence"]) < LOW_CONFIDENCE_THRESHOLD for row in rows
        ),
        "high_priority_records": sum(priority(row) == "High" for row in rows),
        "error_reason_counts": Counter(
            row["error_reason"] or "No error" for row in rows
        ),
    }


def write_outputs(rows: list[dict[str, str]], summary: dict) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    enriched = [
        {**row, "category_match": category_match(row), "priority": priority(row)}
        for row in rows
    ]

    with (OUTPUT_DIR / "enriched_review_queue.csv").open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=enriched[0].keys())
        writer.writeheader()
        writer.writerows(enriched)

    serializable = {**summary, "error_reason_counts": dict(summary["error_reason_counts"])}
    (OUTPUT_DIR / "qa_summary.json").write_text(
        json.dumps(serializable, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    evaluation_rows = load_rows()
    qa_summary = build_summary(evaluation_rows)
    write_outputs(evaluation_rows, qa_summary)
    print(json.dumps({**qa_summary, "error_reason_counts": dict(qa_summary["error_reason_counts"])}, indent=2))
