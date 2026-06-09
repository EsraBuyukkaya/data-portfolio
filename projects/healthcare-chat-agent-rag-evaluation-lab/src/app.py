from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"
RESULTS_PATH = OUTPUT_DIR / "evaluation_results.csv"
SUMMARY_PATH = OUTPUT_DIR / "experiment_summary.json"
KB_DIR = ROOT / "data" / "knowledge_base"


def ensure_outputs() -> None:
    if not RESULTS_PATH.exists() or not SUMMARY_PATH.exists():
        subprocess.run([sys.executable, str(ROOT / "src" / "rag_eval.py")], check=True)


@st.cache_data
def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    ensure_outputs()
    results = pd.read_csv(RESULTS_PATH)
    summary = pd.DataFrame(json.loads(SUMMARY_PATH.read_text(encoding="utf-8")))
    return results, summary


def load_knowledge_base() -> pd.DataFrame:
    rows = []
    for path in sorted(KB_DIR.glob("*.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        heading = next((line.replace("#", "").strip() for line in lines if line.startswith("#")), path.stem)
        text = " ".join(line.strip() for line in lines if line.strip() and not line.startswith("#"))
        rows.append({"source": path.name, "topic": heading, "approved_context": text})
    return pd.DataFrame(rows)


st.set_page_config(page_title="Healthcare Chat Agent RAG Evaluation Lab", layout="wide")
results_df, summary_df = load_data()

st.title("Healthcare Chat Agent RAG Evaluation Lab")
st.caption("Python RAG-style retrieval, prompt regression testing, and healthcare AI guardrail evaluation.")
st.info(
    "Scenario: A healthcare team wants to improve a patient support chat assistant, but needs evidence that a new prompt improves safety, escalation, and required workflow language before rollout."
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Prompt Variants", summary_df["prompt_version"].nunique())
col2.metric("Regression Tests", int(summary_df["test_cases"].max()))
col3.metric("Best Overall Pass", f"{summary_df['overall_pass_rate'].max():.1f}%")
col4.metric("Best Safety Pass", f"{summary_df['safety_pass_rate'].max():.1f}%")

tab_demo, tab_results, tab_tests, tab_kb, tab_explain = st.tabs(
    ["Chat Demo", "Experiment Results", "Regression Tests", "Knowledge Base", "How To Explain"]
)

with tab_demo:
    st.header("Chat Demo")
    variant = st.selectbox("Prompt variant", summary_df["prompt_version"].tolist(), index=1)
    variant_rows = results_df[results_df["prompt_version"] == variant]
    question = st.selectbox("Patient question", variant_rows["patient_question"].tolist())
    selected = variant_rows[variant_rows["patient_question"] == question].iloc[0]
    st.subheader("Structured Assistant Output")
    st.json(
        {
            "prompt_version": selected["prompt_version"],
            "question": selected["patient_question"],
            "answer": selected["answer"],
            "retrieved_topic": selected["retrieved_topic"],
            "retrieval_score": selected["retrieval_score"],
            "source": selected["top_source"],
            "overall_pass": bool(selected["overall_pass"]),
        }
    )
    st.subheader("Retrieved Context")
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "source": selected["top_source"],
                    "topic": selected["retrieved_topic"],
                    "context": selected["retrieved_context"],
                }
            ]
        ),
        use_container_width=True,
        hide_index=True,
    )

with tab_results:
    st.header("Experiment Results")
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
    chart_df = summary_df.set_index("variant_name")[
        ["required_wording_pass_rate", "safety_pass_rate", "escalation_pass_rate", "overall_pass_rate"]
    ]
    st.bar_chart(chart_df)
    st.markdown(
        "The revised prompt improves safety, escalation, and required wording while using the same knowledge base. That makes the recommendation evidence-backed instead of opinion-based."
    )

with tab_tests:
    st.header("Regression Tests")
    display_cols = [
        "prompt_version",
        "test_id",
        "expected_topic",
        "retrieved_topic",
        "required_phrase",
        "retrieval_pass",
        "required_wording_pass",
        "safety_pass",
        "escalation_pass",
        "overall_pass",
    ]
    st.dataframe(results_df[display_cols], use_container_width=True, hide_index=True)

with tab_kb:
    st.header("Knowledge Base")
    st.dataframe(load_knowledge_base(), use_container_width=True, hide_index=True)

with tab_explain:
    st.header("How To Explain")
    st.markdown(
        """
        I built this as a local experiment lab for prompt changes. The project uses approved healthcare support notes as the knowledge base, retrieves the most relevant context for each patient question, and compares two prompt variants against regression tests.

        The important part is not just that the assistant answers. The important part is that every answer is scored for retrieval quality, required wording, safety behavior, and escalation behavior. That is how an AI team can decide whether a prompt change is safe enough to pilot.

        In production, I would connect this harness to real chat transcripts after privacy review, add human reviewer labels, track prompt versions, and run statistical analysis before rollout.
        """
    )
