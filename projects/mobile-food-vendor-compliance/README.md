# Mobile Food Vendor Compliance Assistant

## Scenario

A local compliance consulting team is helping mobile food vendors understand permit requirements, inspection risk, and food-safety rules in Suffolk County, New York.

The team needs a practical AI/data tool that can combine public inspection records, regulations, weather data, and permit rules into one workflow for risk scoring, compliance guidance, and question answering.

This project is the outcome of that scenario: an academic team capstone that turns public regulatory data into an interactive compliance assistant.

Full case study: [CASE_STUDY.md](CASE_STUDY.md)

Interview preparation notes: [INTERVIEW_QA.md](INTERVIEW_QA.md)

## Team Credit

This was a collaborative capstone project for `AIM 490W: AI Management Capstone Project`.

| Team Member | Role |
|---|---|
| Aisha | Data Architect Lead |
| Esra | Project idea contributor and NLP Extraction Specialist |
| Laiba | Front-End Experience Lead |

I am presenting this in my portfolio as a team project. The original idea was mine, and the implementation was built collaboratively.

## What The Project Does

- Ingests public inspection, regulation, and weather data.
- Cleans and prepares violation records.
- Extracts regulatory rules from public food-vendor guidance.
- Engineers inspection-risk features.
- Trains a Gradient Boosting classifier to predict high-risk inspection scenarios.
- Generates vendor scenario predictions and recommended actions.
- Provides a Streamlit interface with vendor search, risk scoring, permit checklist, model information, and a RAG-style assistant.
- Produces a technical compliance report.

## Data Sources

| Source | Purpose |
|---|---|
| Suffolk County public restaurant violation records | Historical inspection and violation data |
| NOAA weather data | Weather context for inspection-risk features |
| NY Health Data Portal | Additional NY food inspection context |
| NYC DOH Mobile Food Vendor Regulations PDF | Regulatory text for rule extraction and RAG |
| NY State Sanitary Code Subpart 14-4 | Food-service regulatory references |
| Curated permit bank | Permit checklist logic |

Large raw and processed datasets are not committed to this portfolio repo. The source scripts document how the pipeline ingests and rebuilds the data from public sources.

## Key Results

| Metric | Result |
|---|---|
| Inspection violation records processed | 107,843 |
| Unique facilities represented | 4,977 |
| Extracted regulatory rules | 21 |
| Model | GradientBoostingClassifier |
| ROC AUC | 0.859 |
| PR AUC | 0.673 |
| Lift over base-rate PR baseline | 2.5x |

## Project Structure

```text
mobile-food-vendor-compliance/
  app.py
  requirements.txt
  src/
    01_ingest.py
    02_clean.py
    03_extract_rules.py
    04_features.py
    05_model.py
    06_predict.py
    07_rag.py
    build_report.py
  rules/
    extracted_rules.json
    required_permits.json
  outputs/
    stage*_report.json
    stage6_predictions.json
  assets/
    reports/
      Mobile_Food_Vendor_Compliance_Report.pdf
  data/
    README.md
```

## Pipeline

| Stage | Script | Purpose |
|---|---|---|
| 1 | `src/01_ingest.py` | Fetch public data sources |
| 2 | `src/02_clean.py` | Normalize and clean inspection records |
| 3 | `src/03_extract_rules.py` | Extract structured rules from regulatory text |
| 4 | `src/04_features.py` | Create leak-safe model features |
| 5 | `src/05_model.py` | Train and evaluate the risk model |
| 6 | `src/06_predict.py` | Score vendor scenarios and generate recommended actions |
| 7 | `src/07_rag.py` | Retrieve regulation passages for compliance Q&A |

Each stage writes a JSON report in `outputs/` so the pipeline can be audited.

## Report

The submitted technical report is included here:

[Mobile Food Vendor Compliance Report](assets/reports/Mobile_Food_Vendor_Compliance_Report.pdf)

## How To Run

Install requirements:

```bash
pip install -r requirements.txt
```

Run the pipeline:

```bash
python src/01_ingest.py
python src/02_clean.py
python src/03_extract_rules.py
python src/04_features.py
python src/05_model.py
python src/06_predict.py
```

Launch the Streamlit app:

```bash
python -m streamlit run app.py
```

Optional: set an `ANTHROPIC_API_KEY` in a local `.env` file to enable the LLM answer-generation layer. Without a key, the assistant can fall back to retrieval-only mode.

## Portfolio Story

This project shows my ability to connect AI management, public data, compliance workflows, NLP, predictive modeling, and user-facing application design. It also shows that I can contribute to a team project, document a technical workflow, and explain how an AI system can support operational decision-making.
