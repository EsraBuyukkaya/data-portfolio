# Interview Q&A: Mobile Food Vendor Compliance Assistant

## How would you describe this project?

This was an AI management capstone project where my team built a compliance assistant for mobile food vendors in Suffolk County, New York. The system combines public inspection data, regulatory text, predictive modeling, and a Streamlit interface to help vendors understand compliance risk and permit requirements.

## Was this an individual project or a team project?

It was a team project. The original project idea was mine, and the implementation was built collaboratively with classmates. The report credits Aisha as Data Architect Lead, me as NLP Extraction Specialist, and Laiba as Front-End Experience Lead.

## What was your role?

I contributed the project idea and worked on the NLP/regulatory extraction side. I also helped frame the project around compliance operations and AI management: what problem we were solving, what data sources mattered, and how the final tool could support decision-making.

## What problem were you solving?

Mobile food vendors face fragmented compliance requirements. They may need to understand permits, food-safety rules, inspection history, and risk factors across multiple public sources. The project brings those sources into one workflow.

## What data did the project use?

The project used public Suffolk County inspection records, NOAA weather data, NY food inspection context data, mobile food vendor regulations, NY State Sanitary Code references, and a curated permit bank.

## What does the model predict?

The model predicts higher-risk inspection scenarios using historical violation patterns and engineered features. Because the source data did not include a clean critical/non-critical label, the project used a proxy target based on top-quartile violation count per inspection visit.

## How well did the model perform?

The Gradient Boosting classifier achieved:

- ROC AUC: 0.859
- PR AUC: 0.673
- about 2.5x lift over the base-rate PR baseline

## What makes this an AI project?

It includes several AI/data components:

- NLP-based rule extraction,
- predictive modeling,
- retrieval-based compliance Q&A,
- scenario scoring,
- and an interactive decision-support interface.

## What makes this an AI management project?

It is not just a model. It connects a business/compliance problem to data sources, user needs, workflow design, model evaluation, explainability, and adoption considerations. That is the management layer: understanding how AI fits into an operational process.

## What was difficult?

The hardest part was connecting imperfect public data to a realistic compliance use case. The data was not mobile-vendor-only, severity labels were limited, and regulations came from multiple sources. Those constraints forced us to document assumptions and limitations clearly.

## What would you improve next?

I would:

- narrow the data to mobile food vendors,
- add more jurisdiction-specific permit rules,
- improve rule extraction,
- add a better vendor onboarding flow,
- deploy the app,
- and add model monitoring if the tool were used over time.

## Can this be used in production?

Not as-is. It is a capstone prototype. A production version would need verified legal/compliance review, stronger data filters, current permit fees, authentication, monitoring, and human oversight.

## How would you explain this project to a recruiter?

I would say:

> My team built an AI compliance assistant for mobile food vendors using public inspection records, regulatory text, weather data, machine learning, and a Streamlit app. My idea was to turn fragmented compliance information into a decision-support workflow. I focused on the NLP/regulatory extraction side and helped frame the project as an AI management solution.
