# Case Study

## Business Problem

A healthcare mobile platform supports members who may have unreliable phone service, limited data, or difficulty staying connected to care. The product team wants better visibility into engagement and a workflow that recommends outreach before a member becomes disconnected.

## Objective

Build a privacy-safe prototype that helps a product team:

- monitor member engagement
- identify members at risk
- compare outreach performance
- recommend next-best actions
- explain product insights to non-technical stakeholders

## Approach

I created synthetic member, event, and outreach data to represent a healthcare engagement product. I then used SQLite for product analytics and Streamlit for a dashboard that summarizes member behavior and recommended actions.

## Data Model

| Table | Purpose |
|---|---|
| members | Member profile, plan type, phone reliability, renewal timing |
| events | App usage, appointments, support tickets, renewals |
| outreach | Messages sent by SMS, phone, and app notification |

## Recommendation Logic

The prototype uses transparent rules so stakeholders can understand the decision logic:

- Renewal due soon and low app activity: send renewal reminder.
- Missed appointment and low engagement: offer scheduling support.
- Multiple support tickets: route to support follow-up.
- Low phone reliability: prefer app notification or case manager call.

## Results

The project produces:

- engagement KPIs
- member risk segments
- outreach channel performance
- a prioritized member action list
- a stakeholder-friendly dashboard

## Limitations

This is a portfolio prototype, not a production healthcare system. It uses synthetic data and rule-based recommendations. A real implementation would require HIPAA-compliant data handling, security review, user testing, monitoring, and model validation.

## What I Would Improve Next

- Add cohort retention analysis.
- Add Power BI dashboard version.
- Add experiment tracking for outreach nudges.
- Add a reviewed LLM layer for message drafting.
- Add role-based access and audit logs for a production-style workflow.
