from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "healthcare_etl.db"
OUTPUT_DIR = PROJECT_ROOT / "outputs"


st.set_page_config(page_title="Healthcare Data Quality ETL", layout="wide")


@st.cache_data
def query(sql: str) -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(sql, conn)


def ensure_outputs_exist() -> None:
    if not DB_PATH.exists() or not (OUTPUT_DIR / "data_quality_report.csv").exists():
        st.error("Pipeline outputs not found. Run `python src/generate_data.py` and `python src/run_etl.py` first.")
        st.stop()


ensure_outputs_exist()

summary = json.loads((OUTPUT_DIR / "pipeline_summary.json").read_text(encoding="utf-8"))
quality_report = pd.read_csv(OUTPUT_DIR / "data_quality_report.csv")

st.title("Healthcare Data Quality & ETL Pipeline")
st.caption("Healthcare data analyst prototype for ETL, data validation, SQL modeling, and reporting readiness.")

st.info(
    "Scenario: A healthcare data strategy team needs to validate raw EHR-style data, build analytics-ready tables, "
    "and communicate data reliability to analysts and business users."
)

checks_run = summary["checks_run"]
checks_with_issues = summary["checks_with_issues"]
failed_rows_total = summary["failed_rows_total"]
raw_rows_total = sum(summary["raw_rows"].values())
quality_score = round(((raw_rows_total - failed_rows_total) / raw_rows_total) * 100, 1)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Raw Rows Loaded", f"{sum(summary['raw_rows'].values()):,}")
col2.metric("Analytics Rows", f"{sum(summary['analytics_rows'].values()):,}")
col3.metric("Issues Found", f"{failed_rows_total}")
col4.metric("Quality Score", f"{quality_score}%")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Pipeline Summary", "Data Quality Checks", "Analytics Tables", "SQL Examples", "How To Explain"]
)

with tab1:
    st.subheader("Pipeline Summary")
    left, right = st.columns(2)
    left.write("Raw rows")
    left.dataframe(pd.DataFrame([summary["raw_rows"]]).T.rename(columns={0: "rows"}), use_container_width=True)
    right.write("Analytics rows")
    right.dataframe(pd.DataFrame([summary["analytics_rows"]]).T.rename(columns={0: "rows"}), use_container_width=True)

    encounter_by_class = query(
        """
        SELECT encounter_class, COUNT(*) AS encounters
        FROM fact_encounter
        GROUP BY encounter_class
        ORDER BY encounters DESC;
        """
    )
    st.write("Encounters by class")
    st.bar_chart(encounter_by_class.set_index("encounter_class")["encounters"])

with tab2:
    st.subheader("Data Quality Checks")
    st.dataframe(quality_report, use_container_width=True)
    st.write("Rows with issues are identified and excluded before data reaches analytics tables.")

with tab3:
    st.subheader("Analytics-Ready Tables")
    top_conditions = query(
        """
        SELECT condition_description, COUNT(*) AS condition_count
        FROM fact_condition
        GROUP BY condition_description
        ORDER BY condition_count DESC;
        """
    )
    patient_preview = query("SELECT * FROM dim_patient LIMIT 10;")
    encounter_preview = query("SELECT * FROM fact_encounter LIMIT 10;")
    left, right = st.columns(2)
    left.write("Top conditions")
    left.dataframe(top_conditions, use_container_width=True)
    right.write("Patient dimension preview")
    right.dataframe(patient_preview, use_container_width=True)
    st.write("Encounter fact preview")
    st.dataframe(encounter_preview, use_container_width=True)

with tab4:
    st.subheader("SQL Examples")
    orphan_query = """
    SELECT
      e.encounter_id,
      e.patient_id
    FROM raw_encounters e
    LEFT JOIN raw_patients p ON p.patient_id = e.patient_id
    WHERE p.patient_id IS NULL;
    """
    st.code(orphan_query, language="sql")
    st.dataframe(query(orphan_query), use_container_width=True)

    window_query = """
    SELECT
      patient_id,
      encounter_id,
      start_date,
      ROW_NUMBER() OVER (PARTITION BY patient_id ORDER BY start_date) AS encounter_number
    FROM fact_encounter
    ORDER BY patient_id, encounter_number
    LIMIT 25;
    """
    st.code(window_query, language="sql")
    st.dataframe(query(window_query), use_container_width=True)

with tab5:
    st.subheader("How To Explain This Project")
    st.write(
        "I built this project to demonstrate healthcare ETL and data quality work. It loads raw EHR-style files, "
        "runs validation checks, creates staging tables, builds analytics-ready tables, and shows the results in a dashboard."
    )
    st.write(
        "The important part is not that the data is huge. The important part is that the workflow protects downstream analysts "
        "from bad data by checking keys, dates, duplicates, orphan records, and out-of-range clinical values."
    )
