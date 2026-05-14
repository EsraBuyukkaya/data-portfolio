from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

from launch_advisor import recommend_launch_action


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "launch_command_center.db"


st.set_page_config(page_title="AI Agent Launch Command Center", layout="wide")


@st.cache_data
def query(sql: str) -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(sql, conn)


def ensure_data_exists() -> None:
    if not DB_PATH.exists():
        st.error("Database not found. Run `python src/generate_data.py` and `python src/build_database.py` first.")
        st.stop()


ensure_data_exists()

st.title("Enterprise AI Agent Launch Command Center")
st.caption("Customer strategy prototype using real public outreach data plus simulated enterprise AI-agent launch operations.")

st.info(
    "Scenario: A customer strategy team needs to manage multiple AI agent launches, track readiness, "
    "monitor performance, resolve blockers, and prove business impact within the first two weeks."
)

launch_overview = query(
    """
    SELECT
      COUNT(DISTINCT c.customer_id) AS customers,
      SUM(CASE WHEN l.launch_status = 'At Risk' THEN 1 ELSE 0 END) AS at_risk_launches,
      ROUND(AVG(l.readiness_score), 1) AS avg_readiness
    FROM customers c
    JOIN launches l ON l.customer_id = c.customer_id;
    """
).iloc[0]

impact_overview = query(
    """
    SELECT
      ROUND(SUM(a.revenue_influenced), 0) AS revenue_influenced,
      ROUND(SUM(a.minutes_saved), 0) AS minutes_saved
    FROM agent_calls a;
    """
).iloc[0]

contact_overview = query(
    """
    SELECT
      COUNT(*) AS real_contacts,
      ROUND(AVG(converted_flag), 3) AS conversion_rate,
      ROUND(AVG(call_duration_seconds), 1) AS avg_call_duration,
      ROUND(AVG(campaign_contacts), 1) AS avg_campaign_contacts
    FROM bank_marketing_contacts;
    """
).iloc[0]

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Real Contacts", f"{int(contact_overview['real_contacts']):,}")
col2.metric("Conversion Rate", f"{contact_overview['conversion_rate'] * 100:.1f}%")
col3.metric("Customers", f"{int(launch_overview['customers'])}")
col4.metric("At-Risk Launches", f"{int(launch_overview['at_risk_launches'])}")
col5.metric("Revenue Influenced", f"${int(impact_overview['revenue_influenced']):,}")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Real Outreach Data", "Launch Health", "Agent Performance", "Blockers & Roadmap", "Action Queue"]
)

with tab1:
    st.subheader("Real Customer Outreach Data")
    st.write(
        "This tab uses the UCI Bank Marketing dataset: real public phone-based campaign data from a Portuguese banking institution."
    )
    segment_performance = query(
        """
        SELECT
          job,
          contact,
          COUNT(*) AS contacts,
          ROUND(AVG(converted_flag), 3) AS conversion_rate,
          ROUND(AVG(call_duration_seconds), 1) AS avg_call_duration_seconds,
          ROUND(AVG(campaign_contacts), 1) AS avg_campaign_contacts
        FROM bank_marketing_contacts
        GROUP BY job, contact
        HAVING contacts >= 100
        ORDER BY conversion_rate DESC
        LIMIT 20;
        """
    )
    month_performance = query(
        """
        SELECT
          month,
          COUNT(*) AS contacts,
          ROUND(AVG(converted_flag), 3) AS conversion_rate
        FROM bank_marketing_contacts
        GROUP BY month
        ORDER BY conversion_rate DESC;
        """
    )
    left, right = st.columns(2)
    left.write("Top outreach segments")
    left.dataframe(segment_performance, use_container_width=True)
    right.write("Conversion by month")
    right.dataframe(month_performance, use_container_width=True)
    st.bar_chart(segment_performance.set_index("job")["conversion_rate"])

with tab2:
    st.subheader("Launch Health")
    launch_health = query(
        """
        SELECT
          c.customer_name,
          c.industry,
          l.launch_status,
          l.readiness_score,
          l.qa_pass_rate,
          l.days_to_go_live,
          COUNT(b.blocker_id) AS open_blockers
        FROM launches l
        JOIN customers c ON c.customer_id = l.customer_id
        LEFT JOIN blockers b
          ON b.customer_id = l.customer_id
          AND b.status != 'Closed'
        GROUP BY c.customer_name, c.industry, l.launch_status, l.readiness_score, l.qa_pass_rate, l.days_to_go_live
        ORDER BY l.readiness_score ASC;
        """
    )
    st.dataframe(launch_health, use_container_width=True)
    st.bar_chart(launch_health.set_index("customer_name")["readiness_score"])

with tab3:
    st.subheader("AI Agent Performance")
    performance = query(
        """
        SELECT
          agent_use_case,
          COUNT(*) AS calls,
          ROUND(AVG(contained), 3) AS containment_rate,
          ROUND(AVG(escalated), 3) AS escalation_rate,
          ROUND(AVG(customer_sentiment), 2) AS avg_sentiment,
          ROUND(SUM(revenue_influenced), 0) AS revenue_influenced
        FROM agent_calls
        GROUP BY agent_use_case
        ORDER BY revenue_influenced DESC;
        """
    )
    st.dataframe(performance, use_container_width=True)
    st.bar_chart(performance.set_index("agent_use_case")["containment_rate"])

with tab4:
    st.subheader("Blockers & Roadmap Feedback")
    blockers = query(
        """
        SELECT
          roadmap_category,
          severity,
          COUNT(*) AS blocker_count
        FROM blockers
        WHERE status != 'Closed'
        GROUP BY roadmap_category, severity
        ORDER BY blocker_count DESC;
        """
    )
    blocker_detail = query(
        """
        SELECT
          c.customer_name,
          b.severity,
          b.status,
          b.owner,
          b.roadmap_category,
          b.blocker_summary
        FROM blockers b
        JOIN customers c ON c.customer_id = b.customer_id
        WHERE b.status != 'Closed'
        ORDER BY
          CASE b.severity
            WHEN 'Critical' THEN 1
            WHEN 'High' THEN 2
            WHEN 'Medium' THEN 3
            ELSE 4
          END;
        """
    )
    st.write("Roadmap themes")
    st.dataframe(blockers, use_container_width=True)
    st.write("Open blocker detail")
    st.dataframe(blocker_detail, use_container_width=True)

with tab5:
    st.subheader("Customer Strategy Action Queue")
    action_base = query(
        """
        SELECT
          c.customer_name,
          c.industry,
          l.launch_status,
          l.readiness_score,
          l.qa_pass_rate,
          l.days_to_go_live,
          COALESCE(b.open_blockers, 0) AS open_blockers,
          COALESCE(a.containment_rate, 0) AS containment_rate
        FROM customers c
        JOIN launches l ON l.customer_id = c.customer_id
        LEFT JOIN (
          SELECT customer_id, COUNT(*) AS open_blockers
          FROM blockers
          WHERE status != 'Closed'
          GROUP BY customer_id
        ) b ON b.customer_id = c.customer_id
        LEFT JOIN (
          SELECT customer_id, ROUND(AVG(contained), 3) AS containment_rate
          FROM agent_calls
          GROUP BY customer_id
        ) a ON a.customer_id = c.customer_id
        ORDER BY l.readiness_score ASC, open_blockers DESC;
        """
    )
    rows = []
    for _, row in action_base.iterrows():
        row_dict = row.to_dict()
        action, reason = recommend_launch_action(row_dict)
        rows.append({**row_dict, "recommended_action": action, "reason": reason})
    st.dataframe(pd.DataFrame(rows), use_container_width=True)
