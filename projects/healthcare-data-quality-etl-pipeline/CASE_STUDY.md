# Case Study

## Business Problem

Healthcare analysts need accurate, complete, and reliable data. If patient, encounter, condition, or observation records contain missing keys, invalid dates, duplicate records, or impossible values, downstream reporting becomes unreliable.

## Objective

Build a local ETL and data quality workflow that:

- loads raw healthcare-style files
- validates source data
- documents failed checks
- creates cleaned staging tables
- creates analytics-ready tables
- communicates data reliability to analysts

## Approach

I generated Synthea-style synthetic healthcare records and intentionally included a few common data quality problems. I then built a Python and SQLite pipeline to load, validate, clean, and transform the data.

## Data Model

| Layer | Tables | Purpose |
|---|---|---|
| Raw | raw_patients, raw_encounters, raw_conditions, raw_observations | Preserve source data as received |
| Staging | stg_patients, stg_encounters, stg_conditions, stg_observations | Cleaned records that pass core validation |
| Analytics | dim_patient, fact_encounter, fact_condition, fact_observation | Reporting-ready tables for analysts |

## Data Quality Checks

| Check | Purpose |
|---|---|
| Duplicate patient IDs | Prevent duplicate dimension records |
| Orphan encounters | Find encounters without a valid patient |
| Invalid encounter dates | Catch stop dates before start dates |
| Orphan observations | Find observations without a valid encounter |
| Out-of-range observations | Catch impossible lab/vital values |
| Missing required IDs | Ensure core keys are present |

## Results

The project produces:

- a data quality report
- clear remediation actions for each failed source-data rule
- a SQLite database
- cleaned staging tables
- analytics-ready tables
- a dashboard for pipeline and data quality monitoring

## Limitations

This is a portfolio prototype. It does not process real patient data and is not a production healthcare data platform. A production version would require secure infrastructure, PHI controls, audit logging, automated orchestration, access control, and formal governance review.

## What I Would Improve Next

- Add Power BI/Tableau reporting.
- Add automated unit tests.
- Add schema versioning and migrations.
- Add a simple lineage diagram.
- Add FHIR/HL7 mapping notes.
- Run a larger official Synthea export.
