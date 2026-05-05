from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from contract_review import review_contract
from evaluate_review import evaluate


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIRS = [
    PROJECT_ROOT / "data" / "sample_contracts",
    PROJECT_ROOT / "data" / "cuad_samples",
]


EXPECTED_LABELS_BY_CONTRACT = {
    "ABILITYINC_06_15_2020-EX-4.25-SERVICES_AGREEMENT.txt": PROJECT_ROOT
    / "data"
    / "cuad_labels"
    / "ability_expected_labels.json",
    "CerenceInc_20191002_8-K_EX-10.4_11827494_EX-10.4_Intellectual_Property_Agreement.txt": PROJECT_ROOT
    / "data"
    / "cuad_labels"
    / "cerence_expected_labels.json",
    "ConformisInc_20191101_10-Q_EX-10.6_11861402_EX-10.6_Development_Agreement.txt": PROJECT_ROOT
    / "data"
    / "cuad_labels"
    / "conformis_expected_labels.json",
}


def available_contracts() -> list[Path]:
    contracts: list[Path] = []
    for sample_dir in SAMPLE_DIRS:
        if sample_dir.exists():
            contracts.extend(sorted(sample_dir.glob("*.txt")))
    return sorted(
        contracts,
        key=lambda path: (
            0 if path.name in EXPECTED_LABELS_BY_CONTRACT else 1,
            path.name,
        ),
    )


def status_badge(status: str) -> str:
    if status == "Found":
        return "Found"
    if status == "Missing":
        return "Needs Review"
    return status


def concise_review_note(status: str) -> str:
    if status == "Found":
        return "Detected; verify with reviewer."
    if status == "Missing":
        return "Not detected; reviewer should confirm."
    return "Review recommended."


def get_evaluation_rows(selected: Path, results_path: Path) -> list[dict[str, str]]:
    expected_path = EXPECTED_LABELS_BY_CONTRACT.get(selected.name)
    if not expected_path or not expected_path.exists() or not results_path.exists():
        return []
    return evaluate(expected_path, results_path)


def output_dir_for_contract(selected: Path) -> Path:
    stem = selected.stem.lower()
    if "abilityinc" in stem:
        return PROJECT_ROOT / "outputs" / "cuad_ability_services_agreement"
    if "cerenceinc" in stem:
        return PROJECT_ROOT / "outputs" / "cuad_cerence_intellectual_property_agreement"
    if "conformisinc" in stem:
        return PROJECT_ROOT / "outputs" / "cuad_conformis_development_agreement"
    return PROJECT_ROOT / "outputs"


def render_evaluation(evaluation_rows: list[dict[str, str]]) -> None:
    st.subheader("CUAD Evaluation")
    if evaluation_rows:
        st.dataframe(
            [
                {
                    "Clause Type": row["clause_type"],
                    "Expected": row["expected_status"],
                    "Actual": row["actual_status"],
                    "Evaluation": row["evaluation"],
                    "Note": row["note"],
                }
                for row in evaluation_rows
            ],
            use_container_width=True,
            hide_index=True,
        )
        if any(row["evaluation"] == "Review" for row in evaluation_rows):
            st.warning(
                "One result needs review because the project detector uses a broader clause definition than the CUAD label."
            )
    else:
        st.info("This sample does not have a CUAD expected-label file yet.")


def main() -> None:
    st.set_page_config(page_title="Legal AI Contract Review Assistant", layout="wide")
    st.title("Legal AI Contract Review Assistant")
    st.caption("Scenario prototype for AI-assisted contract review using public CUAD contracts.")

    with st.container(border=True):
        st.markdown(
            "A legal operations team wants to test whether a low-cost prototype can extract key contract clauses, "
            "flag missing terms, and compare selected outputs against expert-labeled public data before adopting a larger AI tool."
        )

    contracts = available_contracts()
    if not contracts:
        st.warning("No contract text files were found.")
        return

    with st.sidebar:
        st.header("Demo Controls")
        selected = st.selectbox(
            "Contract",
            contracts,
            format_func=lambda path: path.name,
        )
        st.markdown("**Review Scope**")
        st.write("Governing Law")
        st.write("Termination")
        st.write("Confidentiality")
        st.write("Indemnification")
        st.write("Limitation of Liability")

    contract_text = selected.read_text(encoding="utf-8")
    results = review_contract(contract_text)
    output_dir = output_dir_for_contract(selected)
    evaluation_rows = get_evaluation_rows(selected, output_dir / "review_results.json")

    found_count = sum(1 for result in results if result.status == "Found")
    missing_count = sum(1 for result in results if result.status == "Missing")
    scored_rows = [row for row in evaluation_rows if row["evaluation"] != "Not Scored"]
    passing_rows = [row for row in scored_rows if row["evaluation"] == "Pass"]

    metric_cols = st.columns(4)
    metric_cols[0].metric("Clauses Checked", len(results))
    metric_cols[1].metric("Found", found_count)
    metric_cols[2].metric("Missing", missing_count)
    metric_cols[3].metric(
        "CUAD Score",
        f"{len(passing_rows)}/{len(scored_rows)}" if scored_rows else "N/A",
    )

    if st.query_params.get("screenshot") == "evaluation":
        render_evaluation(evaluation_rows)
        return

    review_tab, evaluation_tab, contract_tab, explain_tab = st.tabs(
        ["Review", "Evaluation", "Contract Text", "How To Explain"]
    )

    with review_tab:
        st.subheader("Clause Checklist")
        st.dataframe(
            [
                {
                    "Clause Type": result.clause_type,
                    "Status": status_badge(result.status),
                    "Review Note": concise_review_note(result.status),
                }
                for result in results
            ],
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Extracted Clauses")
        for result in results:
            with st.expander(
                f"{result.clause_type}: {status_badge(result.status)}",
                expanded=result.status == "Missing",
            ):
                if result.extracted_text:
                    st.text_area(
                        "Extracted text",
                        result.extracted_text,
                        height=220,
                        label_visibility="collapsed",
                    )
                else:
                    st.info(result.review_note)

    with evaluation_tab:
        render_evaluation(evaluation_rows)

    with contract_tab:
        st.subheader(selected.name)
        st.text_area("Contract text", contract_text, height=520)

    with explain_tab:
        st.subheader("Interview Explanation")
        st.markdown(
            """
            I built this project from a legal AI job-description scenario. The goal was to prototype a first-pass
            contract review assistant using free public data, then validate selected outputs against CUAD expert labels.

            The first version uses transparent rule-based extraction so the results are easy to inspect. Testing on real
            CUAD contracts showed where keyword matching worked and where label definitions mattered, especially for
            termination clauses.
            """
        )
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
