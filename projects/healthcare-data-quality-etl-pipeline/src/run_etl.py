from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
DB_PATH = DATA_DIR / "healthcare_etl.db"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    patients = pd.read_csv(RAW_DIR / "patients.csv", dtype=str).fillna("")
    encounters = pd.read_csv(RAW_DIR / "encounters.csv", dtype=str).fillna("")
    conditions = pd.read_csv(RAW_DIR / "conditions.csv", dtype=str).fillna("")
    observations = pd.read_csv(RAW_DIR / "observations.csv").fillna("")

    quality_report = run_quality_checks(patients, encounters, observations)
    quality_report.to_csv(OUTPUT_DIR / "data_quality_report.csv", index=False)

    stg_patients = patients.drop_duplicates(subset=["patient_id"])
    stg_patients = stg_patients[stg_patients["patient_id"] != ""]
    valid_patient_ids = set(stg_patients["patient_id"])

    stg_encounters = encounters[encounters["patient_id"].isin(valid_patient_ids)].copy()
    stg_encounters = stg_encounters[pd.to_datetime(stg_encounters["stop_date"]) >= pd.to_datetime(stg_encounters["start_date"])]
    valid_encounter_ids = set(stg_encounters["encounter_id"])

    stg_conditions = conditions[
        conditions["patient_id"].isin(valid_patient_ids) & conditions["encounter_id"].isin(valid_encounter_ids)
    ].copy()

    stg_observations = observations[
        observations["patient_id"].isin(valid_patient_ids) & observations["encounter_id"].isin(valid_encounter_ids)
    ].copy()
    stg_observations = stg_observations[~is_out_of_range(stg_observations)]

    dim_patient = stg_patients.copy()
    fact_encounter = stg_encounters.copy()
    fact_condition = stg_conditions.rename(columns={"description": "condition_description"}).copy()
    fact_observation = stg_observations.copy()

    with sqlite3.connect(DB_PATH) as conn:
        save_table(conn, "raw_patients", patients)
        save_table(conn, "raw_encounters", encounters)
        save_table(conn, "raw_conditions", conditions)
        save_table(conn, "raw_observations", observations)
        save_table(conn, "stg_patients", stg_patients)
        save_table(conn, "stg_encounters", stg_encounters)
        save_table(conn, "stg_conditions", stg_conditions)
        save_table(conn, "stg_observations", stg_observations)
        save_table(conn, "dim_patient", dim_patient)
        save_table(conn, "fact_encounter", fact_encounter)
        save_table(conn, "fact_condition", fact_condition)
        save_table(conn, "fact_observation", fact_observation)

    summary = {
        "raw_rows": {
            "patients": int(len(patients)),
            "encounters": int(len(encounters)),
            "conditions": int(len(conditions)),
            "observations": int(len(observations)),
        },
        "analytics_rows": {
            "dim_patient": int(len(dim_patient)),
            "fact_encounter": int(len(fact_encounter)),
            "fact_condition": int(len(fact_condition)),
            "fact_observation": int(len(fact_observation)),
        },
        "checks_with_issues": int((quality_report["failed_rows"] > 0).sum()),
        "failed_rows_total": int(quality_report["failed_rows"].sum()),
        "checks_run": int(len(quality_report)),
    }
    (OUTPUT_DIR / "pipeline_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Created database: {DB_PATH}")
    print(f"Data quality report: {OUTPUT_DIR / 'data_quality_report.csv'}")


def run_quality_checks(patients: pd.DataFrame, encounters: pd.DataFrame, observations: pd.DataFrame) -> pd.DataFrame:
    valid_patient_ids = set(patients.loc[patients["patient_id"] != "", "patient_id"])
    valid_encounter_ids = set(encounters["encounter_id"])

    checks = [
        {
            "check_name": "missing_patient_ids",
            "failed_rows": int((patients["patient_id"] == "").sum()),
            "business_rule": "Every patient record must have a patient_id.",
            "action_taken": "Excluded from staging patient table.",
        },
        {
            "check_name": "duplicate_patient_ids",
            "failed_rows": int(patients.duplicated(subset=["patient_id"]).sum()),
            "business_rule": "Patient IDs should be unique.",
            "action_taken": "Kept first record and excluded duplicate from staging.",
        },
        {
            "check_name": "orphan_encounters",
            "failed_rows": int((~encounters["patient_id"].isin(valid_patient_ids)).sum()),
            "business_rule": "Every encounter must belong to a valid patient.",
            "action_taken": "Excluded orphan encounter from staging/fact table.",
        },
        {
            "check_name": "invalid_encounter_dates",
            "failed_rows": int((pd.to_datetime(encounters["stop_date"]) < pd.to_datetime(encounters["start_date"])).sum()),
            "business_rule": "Encounter stop_date cannot be before start_date.",
            "action_taken": "Excluded invalid encounter from staging/fact table.",
        },
        {
            "check_name": "orphan_observations",
            "failed_rows": int((~observations["encounter_id"].isin(valid_encounter_ids)).sum()),
            "business_rule": "Every observation must belong to a valid encounter.",
            "action_taken": "Excluded orphan observation from staging/fact table.",
        },
        {
            "check_name": "out_of_range_observations",
            "failed_rows": int(is_out_of_range(observations).sum()),
            "business_rule": "Vitals and labs should fall inside expected clinical bounds.",
            "action_taken": "Excluded out-of-range observations from analytics table.",
        },
    ]

    report = pd.DataFrame(checks)
    report["status"] = report["failed_rows"].apply(lambda value: "Pass" if value == 0 else "Issue Found")
    return report[["check_name", "status", "failed_rows", "business_rule", "action_taken"]]


def is_out_of_range(observations: pd.DataFrame) -> pd.Series:
    values = pd.to_numeric(observations["value"], errors="coerce")
    description = observations["description"]
    return (
        ((description == "Systolic Blood Pressure") & ((values < 60) | (values > 240)))
        | ((description == "Body Mass Index") & ((values < 10) | (values > 80)))
        | ((description == "Hemoglobin A1c") & ((values < 3) | (values > 20)))
    )


def save_table(conn: sqlite3.Connection, table_name: str, df: pd.DataFrame) -> None:
    df.to_sql(table_name, conn, if_exists="replace", index=False)


if __name__ == "__main__":
    main()
