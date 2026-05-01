from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


CLAUSE_PATTERNS = {
    "Governing Law": [
        r"governing law",
        r"choice of law",
    ],
    "Termination": [
        r"termination",
        r"term and termination",
    ],
    "Confidentiality": [
        r"confidentiality",
        r"confidential information",
        r"non-disclosure",
    ],
    "Indemnification": [
        r"indemnification",
        r"indemnify",
        r"hold harmless",
    ],
    "Limitation of Liability": [
        r"limitation of liability",
        r"limits? of liability",
        r"liability cap",
        r"consequential damages",
    ],
}


@dataclass
class ClauseResult:
    clause_type: str
    status: str
    extracted_text: str
    review_note: str


def split_sections(contract_text: str) -> list[str]:
    """Split a contract into rough numbered sections."""
    normalized = contract_text.replace("\r\n", "\n")
    matches = list(re.finditer(r"(?m)^\d+\.\s+.+$", normalized))

    if not matches:
        return [normalized.strip()]

    sections = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(normalized)
        sections.append(normalized[start:end].strip())
    return sections


def find_clause(clause_type: str, patterns: list[str], sections: list[str]) -> ClauseResult:
    for section in sections:
        section_lower = section.lower()
        if any(re.search(pattern, section_lower) for pattern in patterns):
            return ClauseResult(
                clause_type=clause_type,
                status="Found",
                extracted_text=section,
                review_note="Clause detected. Review the extracted text for business and legal accuracy.",
            )

    return ClauseResult(
        clause_type=clause_type,
        status="Missing",
        extracted_text="",
        review_note="Clause was not detected in this baseline review. A legal reviewer should confirm whether it is missing or written under a different heading.",
    )


def review_contract(contract_text: str) -> list[ClauseResult]:
    sections = split_sections(contract_text)
    return [
        find_clause(clause_type, patterns, sections)
        for clause_type, patterns in CLAUSE_PATTERNS.items()
    ]


def build_plain_english_summary(results: list[ClauseResult]) -> str:
    found = [result.clause_type for result in results if result.status == "Found"]
    missing = [result.clause_type for result in results if result.status == "Missing"]

    summary_parts = []
    if found:
        summary_parts.append(f"The review detected these key clauses: {', '.join(found)}.")
    if missing:
        summary_parts.append(f"The review did not detect these clauses: {', '.join(missing)}.")
    summary_parts.append(
        "This is a rule-based portfolio prototype, so all results should be treated as a first-pass review rather than legal advice."
    )
    return " ".join(summary_parts)


def render_markdown_report(contract_path: Path, results: list[ClauseResult]) -> str:
    rows = [
        "| Clause Type | Status | Review Note |",
        "|---|---|---|",
    ]

    for result in results:
        rows.append(f"| {result.clause_type} | {result.status} | {result.review_note} |")

    extracted_sections = []
    for result in results:
        if result.extracted_text:
            extracted_sections.append(
                f"### {result.clause_type}\n\n```text\n{result.extracted_text}\n```"
            )

    return f"""# Contract Review Report

## Contract Reviewed

`{contract_path.name}`

## Summary

{build_plain_english_summary(results)}

## Clause Checklist

{chr(10).join(rows)}

## Extracted Clauses

{chr(10).join(extracted_sections)}
"""


def save_outputs(contract_path: Path, output_dir: Path, results: list[ClauseResult]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "review_results.json"
    report_path = output_dir / "review_report.md"

    json_path.write_text(
        json.dumps([asdict(result) for result in results], indent=2),
        encoding="utf-8",
    )
    report_path.write_text(
        render_markdown_report(contract_path, results),
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a baseline contract clause review.")
    parser.add_argument(
        "--contract",
        type=Path,
        default=Path("data/sample_contracts/sample_service_agreement.txt"),
        help="Path to a contract text file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs"),
        help="Directory where review outputs should be saved.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    contract_text = args.contract.read_text(encoding="utf-8")
    results = review_contract(contract_text)
    save_outputs(args.contract, args.output_dir, results)

    print(f"Reviewed {args.contract}")
    print(f"Saved outputs to {args.output_dir}")


if __name__ == "__main__":
    main()
