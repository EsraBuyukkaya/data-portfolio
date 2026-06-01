import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_DIR / "data" / "ecommerce_ops.db"


st.set_page_config(
    page_title="E-Commerce Operations & Logistics Dashboard",
    layout="wide",
)


@st.cache_data
def query(sql: str) -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(sql, conn)


def fmt_pct(value):
    return f"{value:.1f}%"


st.title("E-Commerce Operations & Logistics Command Center")
st.caption("DTC operations analytics prototype using Python, SQLite, SQL, and Streamlit.")
st.info(
    "Scenario: A fast-growing direct-to-consumer apparel brand needs reporting across fulfillment, logistics, returns, "
    "customer support, and backlog risk so leaders can spot issues before they escalate."
)

orders = query("SELECT * FROM orders")
tickets = query("SELECT * FROM support_tickets")
daily = query("SELECT * FROM daily_operations")

orders["order_date"] = pd.to_datetime(orders["order_date"])
tickets["created_date"] = pd.to_datetime(tickets["created_date"])
daily["order_date"] = pd.to_datetime(daily["order_date"])

min_date, max_date = orders["order_date"].min().date(), orders["order_date"].max().date()
with st.sidebar:
    st.header("Controls")
    date_range = st.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    country_filter = st.multiselect("Country", sorted(orders["country"].unique()), default=sorted(orders["country"].unique()))
    carrier_filter = st.multiselect("Carrier", sorted(orders["carrier"].unique()), default=sorted(orders["carrier"].unique()))

if len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
else:
    start_date, end_date = pd.to_datetime(min_date), pd.to_datetime(max_date)

filtered_orders = orders[
    (orders["order_date"].between(start_date, end_date))
    & (orders["country"].isin(country_filter))
    & (orders["carrier"].isin(carrier_filter))
]
filtered_tickets = tickets[tickets["order_id"].isin(filtered_orders["order_id"])]
filtered_daily = daily[daily["order_date"].between(start_date, end_date)]

total_orders = len(filtered_orders)
late_rate = filtered_orders["late_delivery"].mean() * 100 if total_orders else 0
return_rate = filtered_orders["returned"].mean() * 100 if total_orders else 0
ticket_volume = len(filtered_tickets)
sla_breach_rate = filtered_tickets["sla_breached"].mean() * 100 if ticket_volume else 0
cost_to_serve = (filtered_orders["shipping_cost"].sum() + filtered_tickets["ticket_id"].count() * 4.25 + filtered_orders["returned"].sum() * 7.5) / max(total_orders, 1)

metric_cols = st.columns(6)
metric_cols[0].metric("Orders", f"{total_orders:,}")
metric_cols[1].metric("Late Delivery", fmt_pct(late_rate))
metric_cols[2].metric("Return Rate", fmt_pct(return_rate))
metric_cols[3].metric("Support Tickets", f"{ticket_volume:,}")
metric_cols[4].metric("SLA Breach", fmt_pct(sla_breach_rate))
metric_cols[5].metric("Cost To Serve", f"${cost_to_serve:.2f}")

tab_overview, tab_logistics, tab_cx, tab_risk, tab_sql, tab_explain = st.tabs(
    [
        "Operations Overview",
        "Carrier & Fulfillment",
        "CX Dashboard",
        "Risk Forecast",
        "SQL Metrics",
        "How To Explain",
    ]
)

with tab_overview:
    st.subheader("Operations Overview")
    monthly = (
        filtered_orders.assign(month=filtered_orders["order_date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)
        .agg(
            orders=("order_id", "count"),
            net_revenue=("order_value", "sum"),
            late_rate=("late_delivery", "mean"),
            return_rate=("returned", "mean"),
        )
    )
    monthly["late_rate"] = (monthly["late_rate"] * 100).round(1)
    monthly["return_rate"] = (monthly["return_rate"] * 100).round(1)
    c1, c2 = st.columns(2)
    c1.line_chart(monthly, x="month", y="orders")
    c2.line_chart(monthly, x="month", y="net_revenue")
    st.dataframe(
        monthly.sort_values("month"),
        use_container_width=True,
        hide_index=True,
    )

with tab_logistics:
    st.subheader("Carrier & Fulfillment Performance")
    carrier_perf = (
        filtered_orders.groupby(["carrier", "fulfillment_center"], as_index=False)
        .agg(
            orders=("order_id", "count"),
            avg_delivery_days=("delivery_days", "mean"),
            late_rate=("late_delivery", "mean"),
            avg_shipping_cost=("shipping_cost", "mean"),
            return_rate=("returned", "mean"),
        )
    )
    for col in ["late_rate", "return_rate"]:
        carrier_perf[col] = (carrier_perf[col] * 100).round(1)
    carrier_perf["avg_delivery_days"] = carrier_perf["avg_delivery_days"].round(1)
    carrier_perf["avg_shipping_cost"] = carrier_perf["avg_shipping_cost"].round(2)
    st.dataframe(carrier_perf.sort_values(["late_rate", "avg_shipping_cost"], ascending=False), use_container_width=True, hide_index=True)

    product_returns = (
        filtered_orders.groupby("product_line", as_index=False)
        .agg(orders=("order_id", "count"), return_rate=("returned", "mean"), revenue=("order_value", "sum"))
    )
    product_returns["return_rate"] = (product_returns["return_rate"] * 100).round(1)
    product_returns["revenue"] = product_returns["revenue"].round(0)
    st.bar_chart(product_returns.sort_values("return_rate", ascending=False), x="product_line", y="return_rate")

with tab_cx:
    st.subheader("Customer Experience Dashboard")
    ticket_category = (
        filtered_tickets.groupby(["category", "channel"], as_index=False)
        .agg(tickets=("ticket_id", "count"), sla_breach_rate=("sla_breached", "mean"), avg_resolution_hours=("resolution_hours", "mean"))
    )
    if not ticket_category.empty:
        ticket_category["sla_breach_rate"] = (ticket_category["sla_breach_rate"] * 100).round(1)
        ticket_category["avg_resolution_hours"] = ticket_category["avg_resolution_hours"].round(1)
    st.dataframe(ticket_category.sort_values("tickets", ascending=False), use_container_width=True, hide_index=True)

    agent_perf = (
        filtered_tickets.groupby("agent", as_index=False)
        .agg(tickets=("ticket_id", "count"), avg_first_response=("first_response_hours", "mean"), sla_breach_rate=("sla_breached", "mean"))
    )
    if not agent_perf.empty:
        agent_perf["avg_first_response"] = agent_perf["avg_first_response"].round(1)
        agent_perf["sla_breach_rate"] = (agent_perf["sla_breach_rate"] * 100).round(1)
    st.bar_chart(agent_perf.sort_values("tickets", ascending=False), x="agent", y="tickets")

with tab_risk:
    st.subheader("Backlog & Launch Risk Forecast")
    risk_view = filtered_daily.sort_values("backlog_risk_score", ascending=False).head(20)
    st.dataframe(
        risk_view[
            [
                "order_date",
                "orders",
                "tickets",
                "late_rate",
                "return_rate",
                "expected_ticket_volume",
                "sla_breaches",
                "backlog_risk_score",
                "risk_level",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )
    st.bar_chart(risk_view.sort_values("order_date"), x="order_date", y="backlog_risk_score")
    st.markdown("**Recommended actions**")
    st.write(
        "- High launch-risk days should trigger staffing review, carrier follow-up, and proactive customer messaging.\n"
        "- Rising late-delivery rates should be reviewed by carrier and fulfillment center.\n"
        "- Return spikes should be checked by product line and promotion type."
    )

with tab_sql:
    st.subheader("SQL Metrics")
    st.code(
        """
SELECT
    carrier,
    COUNT(*) AS orders,
    ROUND(AVG(delivery_days), 1) AS avg_delivery_days,
    ROUND(AVG(CASE WHEN late_delivery = 1 THEN 1.0 ELSE 0 END) * 100, 1) AS late_delivery_rate,
    ROUND(AVG(shipping_cost), 2) AS avg_shipping_cost
FROM orders
GROUP BY carrier
ORDER BY late_delivery_rate DESC;
        """,
        language="sql",
    )
    sql_result = query(
        """
        SELECT
            carrier,
            COUNT(*) AS orders,
            ROUND(AVG(delivery_days), 1) AS avg_delivery_days,
            ROUND(AVG(CASE WHEN late_delivery = 1 THEN 1.0 ELSE 0 END) * 100, 1) AS late_delivery_rate,
            ROUND(AVG(shipping_cost), 2) AS avg_shipping_cost
        FROM orders
        GROUP BY carrier
        ORDER BY late_delivery_rate DESC
        """
    )
    st.dataframe(sql_result, use_container_width=True, hide_index=True)

with tab_explain:
    st.subheader("How To Explain This Project")
    st.write(
        """
        This project simulates the reporting infrastructure an operations and logistics data analyst might build for a fast-growing
        direct-to-consumer apparel brand. The dashboard connects order, carrier, fulfillment, returns, and support-ticket data into
        one operational view.

        The purpose is to help leaders find issues early: late shipments, return spikes, SLA pressure, expensive carriers, and
        days where support backlog risk is rising.
        """
    )
    st.markdown("**Important limitation:** The data is synthetic because real 3PL, carrier, and CX exports are private. The structure mirrors real operational data feeds.")
