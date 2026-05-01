from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from contract_review import review_contract


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIRS = [
    PROJECT_ROOT / "data" / "sample_contracts",
    PROJECT_ROOT / "data" / "cuad_samples",
]


def available_contracts() -> list[Path]:
    contracts: list[Path] = []
    for sample_dir in SAMPLE_DIRS:
        if sample_dir.exists():
            contracts.extend(sorted(sample_dir.glob("*.txt")))
    return contracts


def main() -> None:
    st.set_page_config(page_title="Legal AI Contract Review Assistant", layout="wide")
    st.title("Legal AI Contract Review Assistant")
    st.caption("Scenario prototype: clause extraction and first-pass contract review using public/sample contracts.")

    contracts = available_contracts()
    if not contracts:
        st.warning("No contract text files were found.")
        return

    selected = st.selectbox(
        "Contract",
        contracts,
        format_func=lambda path: path.name,
    )

    contract_text = selected.read_text(encoding="utf-8")
    results = review_contract(contract_text)

    found_count = sum(1 for result in results if result.status == "Found")
    missing_count = sum(1 for result in results if result.status == "Missing")

    metric_cols = st.columns(3)
    metric_cols[0].metric("Clauses Checked", len(results))
    metric_cols[1].metric("Found", found_count)
    metric_cols[2].metric("Missing", missing_count)

    st.subheader("Clause Checklist")
    st.dataframe(
        [
            {
                "Clause Type": result.clause_type,
                "Status": result.status,
                "Review Note": result.review_note,
            }
            for result in results
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Extracted Clauses")
    for result in results:
        with st.expander(f"{result.clause_type}: {result.status}", expanded=result.status == "Missing"):
            if result.extracted_text:
                st.text(result.extracted_text)
            else:
                st.info(result.review_note)

    st.subheader("JSON Output")
    st.code(
        json.dumps(
            [
                {
                    "clause_type": result.clause_type,
                    "status": result.status,
                    "extracted_text": result.extracted_text,
                    "review_note": result.review_note,
                }
                for result in results
            ],
            indent=2,
        ),
        language="json",
    )


if __name__ == "__main__":
    main()
