# Build Steps

This guide explains how to recreate the project.

## Program To Use

Use these free tools:

| Tool | Why We Use It |
|---|---|
| PowerShell | Run commands |
| Python | Generate data and run ETL |
| SQLite | Store raw, staging, and analytics tables |
| Streamlit | Build the dashboard |
| GitHub | Show the project in the portfolio |

## Step 1: Generate Healthcare Source Data

Run:

```bash
python src/generate_data.py
```

This creates Synthea-style synthetic healthcare CSV files:

- `data/raw/patients.csv`
- `data/raw/encounters.csv`
- `data/raw/conditions.csv`
- `data/raw/observations.csv`

What you should understand:

- These are not real patients.
- The tables imitate common EHR data structures.
- A few intentional quality issues are included so the ETL can catch them.

## Step 2: Run The ETL Pipeline

Run:

```bash
python src/run_etl.py
```

This creates:

- `data/healthcare_etl.db`
- `outputs/data_quality_report.csv`
- `outputs/pipeline_summary.json`

What the ETL does:

- loads raw CSVs
- checks data quality
- removes invalid records from staging
- creates analytics tables
- saves a data quality report

## Step 3: Review The SQL

Open:

```text
sql/data_quality_queries.sql
```

The SQL demonstrates:

- joins
- aggregations
- data quality checks
- orphan record detection
- analytic summary queries

## Step 4: Run The Dashboard

Run:

```bash
python -m streamlit run src/app.py
```

The dashboard shows:

- rows loaded by table
- pass/fail data quality checks
- data quality score
- encounter trends
- top conditions
- analytics-ready table previews

## Step 5: Explain It In An Interview

Short version:

> I built a healthcare ETL and data quality pipeline using Synthea-style synthetic EHR data. The project loads raw patient, encounter, condition, and observation files, runs validation checks, builds cleaned staging tables, creates analytics-ready reporting tables, and displays pipeline health in a Streamlit dashboard.

## What To Add Later

- Power BI or Tableau dashboard
- automated test framework
- schema migration examples
- Databricks or Spark version
- lineage diagram
- HL7/FHIR mapping notes
