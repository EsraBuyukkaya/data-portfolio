# Case Study: Mobile Food Vendor Compliance Assistant

## Scenario

A small compliance consulting team wants to help mobile food vendors reduce inspection risk and understand their permit obligations before operating in Suffolk County, New York.

The problem is fragmented information. Inspection records, weather data, sanitary code requirements, and mobile vending guidance exist in separate public sources. Vendors may not know which permits apply, what rules matter most, or which operational issues increase inspection risk.

## Project Outcome

Our team built an AI/data compliance assistant that combines public data, rule extraction, machine learning, and a Streamlit interface.

The system supports:

- vendor inspection search,
- compliance-risk scoring,
- what-if scenario analysis,
- permit checklist generation,
- regulation browsing,
- model performance review,
- and retrieval-based compliance Q&A.

## My Role

This was a team project. I contributed the original project idea and worked as the NLP Extraction Specialist.

My portfolio framing focuses on:

- turning a real compliance problem into an AI/data project idea,
- supporting regulatory rule extraction,
- connecting the project to AI management and responsible adoption,
- and explaining the business value of the workflow.

## Data And Inputs

The project used public and regulatory data sources:

- Suffolk County public inspection violation records,
- NOAA weather data,
- NY food inspection context data,
- NYC DOH mobile food vendor regulations,
- NY State Sanitary Code Subpart 14-4,
- and a curated permit checklist.

The portfolio version does not commit the large raw datasets. Instead, it includes source scripts, rule files, stage reports, model outputs, and the final report.

## Technical Workflow

1. Ingest public inspection, weather, and regulation sources.
2. Clean and normalize inspection records.
3. Extract relevant regulatory rules using NLP methods.
4. Engineer features for inspection-risk modeling.
5. Train a Gradient Boosting classifier.
6. Score vendor scenarios and generate recommended actions.
7. Use retrieval to answer compliance questions from regulation passages.
8. Present outputs through a Streamlit interface and technical report.

## Results

| Result | Value |
|---|---|
| Violation records processed | 107,843 |
| Unique facilities | 4,977 |
| Extracted rules | 21 |
| Model ROC AUC | 0.859 |
| Model PR AUC | 0.673 |
| Lift over baseline | 2.5x |

## Why This Matters

The project shows how AI can support compliance and operations without replacing human judgment. A vendor or consultant can use the tool to identify risk areas, understand permit obligations, and prepare for inspection review.

The project also shows responsible AI thinking: public data sources, validation reports, explainable model outputs, cited regulatory sources, and documented limitations.

## Limitations

- The data includes broader food-service inspection records, not only mobile vendors.
- Some regulation sources are proxies for town-specific rules.
- Weather coverage does not fully overlap every inspection date.
- The risk target is a proxy based on violation count because critical/non-critical severity labels were not available.
- The app is a local prototype, not a production compliance system.

## Next Improvements

- Filter source data more tightly to mobile food vendors.
- Add jurisdiction-specific permit rules by town.
- Improve regulatory text extraction.
- Add model monitoring and fairness checks.
- Deploy the app with authentication.
- Add a clearer vendor-facing workflow for permit readiness.
