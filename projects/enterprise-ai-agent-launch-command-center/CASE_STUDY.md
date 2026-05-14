# Case Study

## Business Problem

Enterprise AI agent launches move quickly and involve many moving parts: customer data, agent configuration, QA, integrations, call performance, stakeholder alignment, blockers, and executive expectations.

The customer strategy team needs a command center that can show launch status and business impact without waiting for scattered updates.

## Objective

Build a prototype that helps an AI customer strategy team:

- track multiple AI agent launches
- identify at-risk deployments
- monitor AI agent quality
- define measurable business impact
- turn launch issues into roadmap feedback
- communicate status to executives

## Approach

I used the real public UCI Bank Marketing dataset for customer-contact and conversion analytics. I then created synthetic enterprise launch data for readiness, blockers, QA, and AI-agent monitoring because real enterprise AI-agent launch data is not public.

I used SQLite for SQL-based analysis and Streamlit for the command center interface.

## Data Model

| Table | Purpose |
|---|---|
| customers | Customer segment, industry, contract value, launch owner |
| bank_marketing_contacts | Real public customer-contact records and conversion outcomes |
| launches | Kickoff date, go-live target, readiness, QA pass rate, status |
| agent_calls | AI agent call outcomes, intent, sentiment, escalation, revenue influence |
| blockers | Launch blockers, owner, severity, status, roadmap category |

## Launch Advisory Logic

The prototype recommends actions using transparent rules:

- Low readiness and near go-live: executive escalation.
- Low QA pass rate: prioritize agent testing and prompt review.
- High escalation rate: review unresolved intents and handoff design.
- Open critical blocker: assign owner and hold daily launch check-in.
- Strong performance: prepare expansion or additional use case proposal.

## Results

The project produces:

- launch health summary
- real outreach conversion analysis
- customer readiness scores
- AI agent performance metrics
- blocker prioritization
- roadmap feedback themes
- next action recommendations

## Limitations

This is a portfolio prototype. It uses real public outreach data and simulated launch operations data. A production version would need real customer data integrations, permissioning, audit logs, CRM/telephony connections, privacy review, and monitoring for AI quality and compliance.

## What I Would Improve Next

- Add mock CRM and telephony API ingestion.
- Add weekly executive status report export.
- Add customer-level launch notes and decision logs.
- Add customer expansion forecasting.
- Add human-reviewed AI-generated launch summaries.
