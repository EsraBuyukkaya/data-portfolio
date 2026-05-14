# Build Steps

This document explains how to recreate the project from scratch.

## Program To Use

Use these free tools:

| Tool | Why We Use It |
|---|---|
| PowerShell | Run project commands |
| Python | Create data and run the app |
| SQLite | Store the project data locally |
| Streamlit | Build the dashboard |
| GitHub | Show the project in the portfolio |

You do not need AWS, Oracle, Power BI, or a paid AI API for this version.

## Step 1: Create Synthetic Data

Why: real healthcare member data is private. Synthetic data lets us build the same type of workflow safely.

Run:

```bash
python src/generate_data.py
```

This creates:

- `data/synthetic_members.csv`
- `data/synthetic_events.csv`
- `data/synthetic_outreach.csv`

What you should understand:

- `synthetic_members.csv` is the main member table.
- `synthetic_events.csv` stores app usage, appointments, renewals, and support activity.
- `synthetic_outreach.csv` stores messages sent to members and whether they responded.

## Step 2: Build SQLite Database

Run:

```bash
python src/build_database.py
```

This creates:

- `data/member_engagement.db`

What you should understand:

SQLite is a small local database. It lets us practice SQL without needing AWS, Oracle, or a company database.

## Step 3: Review The SQL

Open:

```text
sql/product_metrics.sql
```

The SQL answers product questions:

- How many active members do we have?
- Which plan types have higher engagement risk?
- Which outreach channel performs best?
- Which members need a next action?

## Step 4: Run The Dashboard

Run:

```bash
python -m streamlit run src/app.py
```

Open the local Streamlit link in your browser.

What the dashboard shows:

- engagement KPIs
- risk segments
- outreach performance
- member-level next-best actions
- SQL outputs used by the product team

## Step 5: Explain It In An Interview

Short version:

> I built a synthetic healthcare product analytics project for a mobile health platform scenario. I used Python to generate privacy-safe member behavior data, SQLite to model the data and run SQL analytics, and Streamlit to create a dashboard. The project identifies members at risk of disengagement or missed renewal and recommends the next best outreach action.

## What To Add Later

- Power BI version of the dashboard
- More advanced SQL window functions
- Cohort retention analysis
- A real LLM layer with safe public data
- A/B test analysis for outreach messages
