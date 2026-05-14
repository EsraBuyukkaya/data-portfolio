# Healthcare Member Engagement AI Product Intelligence Hub

## Scenario

A healthcare mobile platform wants to understand which members are at risk of disengaging, missing care, or missing coverage renewal deadlines.

The product team needs a practical way to monitor member engagement, identify risk patterns, and recommend the next best outreach action. This project is the outcome of that scenario: a free, local analytics and AI-workflow prototype built with synthetic healthcare engagement data.

Full case study: [CASE_STUDY.md](CASE_STUDY.md)

Interview preparation notes: [INTERVIEW_QA.md](INTERVIEW_QA.md)

Step-by-step build guide: [BUILD_STEPS.md](BUILD_STEPS.md)

## Project Goal

This project was designed from a Manager, AI Product Innovation job description. The role asked for SQL, product analytics, dashboarding, AI-powered workflows, user behavior analysis, and clear communication with product stakeholders.

The goal is to show how I would help a healthcare product team answer questions like:

- Which members are most at risk of disengaging?
- Which outreach channel is working best?
- Which members need renewal reminders or care scheduling support?
- What product behavior should the team investigate next?

## Job Description Match

| Job Requirement | How This Project Demonstrates It |
|---|---|
| SQL product analytics | Uses SQLite queries with joins, aggregations, and window functions |
| Dashboarding / BI | Builds a Streamlit dashboard for product and operations metrics |
| AI-powered workflows | Creates a rule-based next-best-action recommender that mimics an AI workflow |
| Product intelligence | Connects member behavior, outreach, support tickets, and renewal risk |
| Data infrastructure | Creates synthetic data tables and a local SQLite database |
| User behavior analysis | Tracks app activity, missed appointments, support tickets, and outreach response |
| Healthcare mission awareness | Focuses on access, coverage renewal, care scheduling, and member engagement |
| Clear communication | Includes case study, interview Q&A, and build steps |

## Free Tools Used

- Python
- SQLite
- Streamlit
- pandas
- GitHub

No paid API, AWS account, or real patient data is required.

## Data Privacy Note

This project uses synthetic data only. It does not include real patient names, phone numbers, health records, claims data, or protected health information.

## Project Structure

```text
healthcare-member-engagement-ai/
  README.md
  BUILD_STEPS.md
  CASE_STUDY.md
  INTERVIEW_QA.md
  requirements.txt
  data/
    synthetic_members.csv
    synthetic_events.csv
    synthetic_outreach.csv
    member_engagement.db
  sql/
    product_metrics.sql
  src/
    generate_data.py
    build_database.py
    recommender.py
    app.py
```

## What The Project Does

1. Generates synthetic member engagement data.
2. Builds a local SQLite database.
3. Runs SQL product analytics queries.
4. Scores members for disengagement and renewal risk.
5. Recommends next-best outreach actions.
6. Displays product metrics in a Streamlit dashboard.

## How To Run

From this project folder:

```bash
python src/generate_data.py
python src/build_database.py
python -m streamlit run src/app.py
```

## Portfolio Story

This project shows how I can turn a product/AI job description into a working analytics prototype. It demonstrates SQL, Python, dashboarding, product thinking, and AI-workflow design in a healthcare scenario while staying privacy-safe and free to run locally.
