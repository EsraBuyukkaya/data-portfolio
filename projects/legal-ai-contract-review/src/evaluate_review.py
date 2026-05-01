from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate(expected_path: Path, results_path: Path) -> list[dict[str, str]]:
    expected = load_json(expected_path)
    results = load_json(results_path)
    result_by_clause = {item["clause_type"]: item for item in results}

    evaluation_rows = []
    for label in expected["labels"]:
        clause_type = label["project_clause_type"]
        expected_status = label["expected_status"]

        if expected_status == "Not Scored":
            evaluation_rows.append(
                {
                    "clause_type": clause_type,
                    "expected_status": expected_status,
                    "actual_status": result_by_clause.get(clause_type, {}).get("status", "Not Found"),
                    "evaluation": "Not Scored",
                    "note": label["expected_answer"],
                }
            )
            continue

        actual_status = result_by_clause.get(clause_type, {}).get("status", "Not Found")
        evaluation_rows.append(
            {
                "clause_type": clause_type,
                "expected_status": expected_status,
                "actual_status": actual_status,
                "evaluation": "Pass" if actual_status == expected_status else "Review",
                "note": f"CUAD answer: {label['expected_answer']}",
            }
        )

    return evaluation_rows


def render_markdown(evaluation_rows: list[dict[str, str]]) -> str:
    rows = [
        "| Clause Type | Expected | Actual | Evaluation | Note |",
        "|---|---|---|---|---|",
    ]
    for row in evaluation_rows:
        rows.append(
            f"| {row['clause_type']} | {row['expected_status']} | {row['actual_status']} | {row['evaluation']} | {row['note']} |"
        )

    scored_rows = [row for row in evaluation_rows if row["evaluation"] != "Not Scored"]
    passing_rows = [row for row in scored_rows if row["evaluation"] == "Pass"]

    return f"""# Contract Review Evaluation

## Summary

Scored clauses passed: {len(passing_rows)} of {len(scored_rows)}

This evaluation compares the project's rule-based extraction results against a small answer key derived from CUAD's expert-labeled `master_clauses.csv`.

## Results

{chr(10).join(rows)}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate contract review results against expected labels.")
    parser.add_argument(
        "--expected",
        type=Path,
        default=Path("data/cuad_labels/ability_expected_labels.json"),
        help="Path to expected labels JSON.",
    )
    parser.add_argument(
        "--results",
        type=Path,
        default=Path("outputs/cuad_ability_services_agreement/review_results.json"),
        help="Path to review results JSON.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/cuad_ability_services_agreement/evaluation_report.md"),
        help="Path to save the evaluation report.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    evaluation_rows = evaluate(args.expected, args.results)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_markdown(evaluation_rows), encoding="utf-8")
    print(f"Saved evaluation report to {args.output}")


if __name__ == "__main__":
    main()
