# Interview Q&A

## How would you explain this project?

I built a healthcare ETL and data quality pipeline. It uses Synthea-style synthetic EHR data, loads raw files into SQLite, runs validation checks, creates staging and analytics tables, and displays the pipeline results in Streamlit.

## Why did you use synthetic healthcare data?

Patient-level healthcare data is private and protected. Synthetic EHR data lets me demonstrate healthcare data workflows without exposing real patient information.

## Where is SQL used?

SQL is used to create raw, staging, and analytics tables; join patient and encounter records; detect orphan records; summarize encounters; and support reporting queries.

## What data quality checks are included?

The pipeline checks duplicate patient IDs, missing IDs, orphan encounters, invalid encounter dates, orphan observations, and out-of-range observation values.

## What makes this relevant to healthcare data analyst roles?

The project demonstrates ETL processing, data validation, SQL database design, healthcare-style data, documentation, reporting support, and communication of data reliability issues.

## Is this production-ready?

No. It is a portfolio prototype. A production version would need orchestration, access controls, logging, monitoring, data governance, schema migrations, and secure handling of protected health information.

## How would this help analysts?

It gives analysts cleaner tables, visibility into data quality problems, and reporting-ready outputs. It also documents which checks passed or failed so analysts know whether the data is reliable.

## What did you personally learn?

I learned how to frame a healthcare data analyst job description as a practical ETL project: source data, validation, staging, analytics tables, SQL checks, documentation, and dashboard reporting.
