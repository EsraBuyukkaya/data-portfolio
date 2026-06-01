from __future__ import annotations

import pandas as pd
import streamlit as st

from knowledge_assistant import (
    DEPARTMENT_FILES,
    draft_answer,
    load_passages,
    load_test_cases,
    retrieve,
    run_evaluation,
)


st.set_page_config(page_title="Enterprise AI Knowledge Assistant", layout="wide")


@st.cache_data
def cached_passages():
    return load_passages()


@st.cache_data
def cached_eval():
    return pd.DataFrame(run_evaluation())


passages = cached_passages()
eval_df = cached_eval()

st.title("Enterprise AI Knowledge Assistant & Prompt Evaluation System")
st.caption("Higher-ed enterprise AI prototype using approved knowledge retrieval, guardrails, prompt testing, and lightweight AI operations.")

st.info(
    "Scenario: A university wants an internal AI assistant for Student Services, HR, IT, and Academic teams. "
    "The assistant must answer from approved policy notes, follow institutional tone, avoid unsafe decisions, and pass regression tests before rollout."
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Departments", len(DEPARTMENT_FILES))
col2.metric("Knowledge Passages", len(passages))
col3.metric("Evaluation Tests", len(eval_df))
col4.metric("Pass Rate", f"{(eval_df['evaluation'].eq('Pass').mean() * 100):.0f}%")

tab_assistant, tab_eval, tab_ops, tab_docs, tab_explain = st.tabs(
    ["Assistant Demo", "Evaluation Results", "AI Ops Runbook", "Knowledge Base", "How To Explain"]
)

with tab_assistant:
    st.header("Assistant Demo")
    department = st.selectbox("Department", list(DEPARTMENT_FILES.keys()))
    sample_questions = {
        "Student Services": "How do I withdraw from a class?",
        "HR": "Can you approve my vacation request?",
        "IT": "Can I send you my password so you can fix my login?",
        "Academics": "Can you decide if this student cheated?",
    }
    question = st.text_area("User question", value=sample_questions[department], height=100)

    if st.button("Generate governed answer", type="primary"):
        retrieved = retrieve(question, department, passages)
        answer = draft_answer(question, department, retrieved)
        st.subheader("Structured Assistant Output")
        st.json(answer)
        st.subheader("Retrieved Context")
        st.dataframe(pd.DataFrame(retrieved), use_container_width=True, hide_index=True)

with tab_eval:
    st.header("Evaluation Results")
    st.write("Regression tests check retrieval topic, required policy wording, and safety behavior.")
    st.dataframe(eval_df, use_container_width=True, hide_index=True)

    summary = (
        eval_df.groupby("department")
        .agg(
            tests=("test_id", "count"),
            pass_rate=("evaluation", lambda s: round((s.eq("Pass").mean() * 100), 1)),
            guardrails_triggered=("guardrail_triggered", "sum"),
        )
        .reset_index()
    )
    st.subheader("Department Evaluation Summary")
    st.dataframe(summary, use_container_width=True, hide_index=True)

with tab_ops:
    st.header("AI Ops Runbook")
    runbook = pd.DataFrame(
        [
            {
                "stage": "Prompt change request",
                "owner": "Business + AI owner",
                "control": "Document requested behavior and affected department.",
            },
            {
                "stage": "Regression testing",
                "owner": "AI solutions engineer",
                "control": "Run test cases for accuracy, tone, safety, and policy alignment.",
            },
            {
                "stage": "Knowledge update",
                "owner": "Policy owner",
                "control": "Confirm document source, date, and approval status before ingestion.",
            },
            {
                "stage": "Monitoring",
                "owner": "AI operations",
                "control": "Track fallback rate, low confidence answers, and guardrail triggers.",
            },
            {
                "stage": "Rollback",
                "owner": "AI owner + IT",
                "control": "Restore prior prompt or knowledge version if output quality degrades.",
            },
        ]
    )
    st.dataframe(runbook, use_container_width=True, hide_index=True)

    st.subheader("Example Change Log")
    change_log = pd.DataFrame(
        [
            {
                "version": "v1.0",
                "change": "Initial department prompt framework and policy retrieval.",
                "status": "Approved for prototype",
            },
            {
                "version": "v1.1",
                "change": "Added guardrail wording for passwords, SSNs, financial aid, and formal decisions.",
                "status": "Passed regression tests",
            },
            {
                "version": "v1.2",
                "change": "Planned: add SharePoint document source tracking and owner approval dates.",
                "status": "Backlog",
            },
        ]
    )
    st.dataframe(change_log, use_container_width=True, hide_index=True)

with tab_docs:
    st.header("Knowledge Base")
    docs = []
    for passage in passages:
        docs.append(
            {
                "department": passage.department,
                "source": passage.source,
                "heading": passage.heading,
                "approved_context": passage.text,
            }
        )
    st.dataframe(pd.DataFrame(docs), use_container_width=True, hide_index=True)

with tab_explain:
    st.header("How To Explain This Project")
    st.markdown(
        """
        **Business problem:** A university wants to adopt enterprise AI without giving users unsafe, outdated, or off-policy answers.

        **What I built:** A governed AI assistant prototype that retrieves approved department guidance, drafts structured answers, triggers safety rules, and runs regression tests.

        **Why it matters:** Enterprise AI needs more than prompts. It needs knowledge management, evaluation, tone control, guardrails, monitoring, and rollback planning.

        **What I would improve in production:** Connect approved SharePoint or knowledge base sources, add document owner metadata, use embeddings for retrieval, log user feedback, and route low-confidence answers to human review.
        """
    )
