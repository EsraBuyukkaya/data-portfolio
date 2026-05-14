from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

from recommender import recommend_next_action


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "member_engagement.db"


st.set_page_config(page_title="Healthcare Member Engagement AI", layout="wide")


@st.cache_data
def load_table(table: str) -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(f"SELECT * FROM {table}", conn)


def ensure_data_exists() -> None:
    if not DB_PATH.exists():
        st.error("Database not found. Run `python src/generate_data.py` and `python src/build_database.py` first.")
        st.stop()


ensure_data_exists()
members = load_table("members")
outreach = load_table("outreach")

st.title("Healthcare Member Engagement AI Product Intelligence Hub")
st.caption("Synthetic healthcare product analytics prototype using Python, SQLite, SQL, and Streamlit.")

st.info(
    "Scenario: A healthcare mobile platform wants to identify members at risk of disengagement, "
    "missed care, or missed renewal deadlines, then recommend the next best outreach action."
)

total_members = len(members)
high_risk = int((members["risk_score"] >= 70).sum())
renewal_due = int((members["renewal_due_days"] <= 30).sum())
missed_appt = int(members["missed_appointment_90d"].sum())

col1, col2, col3, col4 = st.columns(4)
col1.metric("Members", f"{total_members:,}")
col2.metric("High Risk", f"{high_risk:,}")
col3.metric("Renewal Due 30 Days", f"{renewal_due:,}")
col4.metric("Missed Appointment", f"{missed_appt:,}")

tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Next Best Actions", "SQL Metrics", "How To Explain"])

with tab1:
    st.subheader("Product Dashboard")
    left, right = st.columns(2)

    risk_by_plan = (
        members.groupby("plan_type", as_index=False)
        .agg(avg_risk_score=("risk_score", "mean"), members=("member_id", "count"))
        .sort_values("avg_risk_score", ascending=False)
    )
    risk_by_plan["avg_risk_score"] = risk_by_plan["avg_risk_score"].round(1)
    left.write("Risk by plan type")
    left.dataframe(risk_by_plan, use_container_width=True)

    response_by_channel = (
        outreach.groupby("channel", as_index=False)
        .agg(messages_sent=("member_id", "count"), response_rate=("responded", "mean"))
        .sort_values("response_rate", ascending=False)
    )
    response_by_channel["response_rate"] = (response_by_channel["response_rate"] * 100).round(1)
    right.write("Outreach response by channel")
    right.dataframe(response_by_channel, use_container_width=True)

    st.bar_chart(risk_by_plan.set_index("plan_type")["avg_risk_score"])

with tab2:
    st.subheader("Member Next-Best-Action Queue")
    action_rows = []
    high_risk_members = members.sort_values("risk_score", ascending=False).head(30)
    for _, row in high_risk_members.iterrows():
        member = row.to_dict()
        action, reason = recommend_next_action(member)
        action_rows.append(
            {
                "member_id": member["member_id"],
                "plan_type": member["plan_type"],
                "risk_score": member["risk_score"],
                "recommended_action": action,
                "reason": reason,
            }
        )
    st.dataframe(pd.DataFrame(action_rows), use_container_width=True)

with tab3:
    st.subheader("SQL Product Metrics")
    st.write("These are examples of product questions this project answers with SQL.")
    with sqlite3.connect(DB_PATH) as conn:
        plan_query = """
        SELECT
          plan_type,
          COUNT(*) AS members,
          ROUND(AVG(risk_score), 1) AS avg_risk_score,
          SUM(CASE WHEN risk_score >= 70 THEN 1 ELSE 0 END) AS high_risk_members
        FROM members
        GROUP BY plan_type
        ORDER BY avg_risk_score DESC;
        """
        st.code(plan_query, language="sql")
        st.dataframe(pd.read_sql_query(plan_query, conn), use_container_width=True)

        channel_query = """
        SELECT
          channel,
          COUNT(*) AS messages_sent,
          SUM(CASE WHEN responded = 1 THEN 1 ELSE 0 END) AS responses,
          ROUND(AVG(responded), 3) AS response_rate
        FROM outreach
        GROUP BY channel
        ORDER BY response_rate DESC;
        """
        st.code(channel_query, language="sql")
        st.dataframe(pd.read_sql_query(channel_query, conn), use_container_width=True)

with tab4:
    st.subheader("How To Explain This Project")
    st.write(
        "I built this as a product analytics and AI-workflow prototype for a healthcare mobile platform. "
        "The project uses synthetic data to avoid privacy issues, SQLite to practice SQL/data modeling, "
        "and Streamlit to create a dashboard for product and operations stakeholders."
    )
    st.write(
        "The AI part is represented as a transparent next-best-action workflow. It looks at member behavior "
        "such as app sessions, renewal timing, missed appointments, support tickets, and phone reliability, "
        "then recommends a practical outreach action."
    )
