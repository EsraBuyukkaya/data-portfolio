# Build Steps

This document explains how to recreate the project and what each part means.

## Program To Use

Use these free tools:

| Tool | Why We Use It |
|---|---|
| PowerShell | Run commands |
| Python | Download public data and generate launch data |
| SQLite | Store customer launch tables locally |
| Streamlit | Build the command center dashboard |
| GitHub | Show the project in the portfolio |

You do not need a paid AI API, Salesforce, or Twilio.

## Step 1: Download Real Public Outreach Data

Run:

```bash
python src/download_real_data.py
```

This downloads the UCI Bank Marketing dataset and creates:

- `data/bank_marketing_contacts.csv`

What you should understand:

- This is real public phone-based marketing campaign data.
- It is useful for outreach/conversion analytics.
- It is not Regal customer data and not private enterprise launch data.

## Step 2: Create Synthetic Customer Launch Data

Run:

```bash
python src/generate_data.py
```

This creates:

- `data/customers.csv`
- `data/launches.csv`
- `data/agent_calls.csv`
- `data/blockers.csv`

What you should understand:

- `customers.csv` is the enterprise customer list.
- `launches.csv` tracks customer kickoff, readiness, QA, and go-live status.
- `agent_calls.csv` simulates AI agent customer communications.
- `blockers.csv` tracks issues that can slow down a launch.

## Step 3: Build The SQLite Database

Run:

```bash
python src/build_database.py
```

This creates:

- `data/launch_command_center.db`

SQLite lets us practice SQL and data modeling for free.

## Step 4: Review The SQL

Open:

```text
sql/launch_metrics.sql
```

The SQL answers customer strategy questions:

- Which launches are at risk?
- Which real outreach segments converted best?
- Which AI agent use cases are performing best?
- Which customers have the biggest business impact?
- Which blockers should leadership prioritize?
- Which issues should become roadmap feedback?

## Step 5: Run The Command Center

Run:

```bash
python -m streamlit run src/app.py
```

The dashboard shows:

- launch readiness
- real outreach conversion metrics
- customer risk
- agent performance
- blocker status
- business impact
- recommended next actions

## Step 6: Explain It In An Interview

Short version:

> I built an AI agent launch command center for a customer strategy scenario. It uses real public customer-contact data from UCI plus simulated enterprise launch data. I used Python, SQLite, SQL, and Streamlit to analyze outreach conversion, track launch readiness, monitor AI-agent performance, manage blockers, and recommend next actions across multiple customer deployments.

## What To Add Later

- Power BI version of the dashboard
- Customer-facing executive summary export
- API mockup for CRM/telephony event ingestion
- More detailed implementation playbook
- LLM-generated launch recap drafts with human review
