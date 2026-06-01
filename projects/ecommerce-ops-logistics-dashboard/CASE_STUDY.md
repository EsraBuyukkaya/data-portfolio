# Case Study: E-Commerce Operations & Logistics Dashboard

## Business Problem

A DTC apparel brand is scaling quickly and needs better visibility into fulfillment performance, returns, customer support workload, and cost to serve. Leadership wants to know where operational issues are emerging before they create customer experience problems.

## Users

- Operations leaders
- Logistics managers
- CX managers
- Supply chain analysts
- BI/data analysts

## Approach

I created synthetic operational data that mirrors common e-commerce data feeds:

- orders
- carrier and delivery performance
- fulfillment centers
- returns
- support tickets
- SLA status
- daily risk indicators

I then loaded the data into SQLite and built a Streamlit dashboard with business-facing tabs.

## Key Decisions

| Decision | Reason |
|---|---|
| Use synthetic operational data | Real 3PL and CX exports are private. |
| Use SQLite | Makes SQL validation and local reproducibility simple. |
| Include CX and logistics together | Cost to serve and customer experience are connected. |
| Add backlog risk score | Shows proactive issue detection rather than passive reporting. |

## Business Value

The dashboard helps a team:

- identify carriers with high late-delivery rates
- monitor fulfillment-center performance
- see which ticket categories create SLA pressure
- understand return patterns by product line
- flag high-risk days for staffing or customer communication
- connect operational quality to CX workload

## What I Would Improve Next

- connect to real warehouse, carrier, and CX exports
- add automated daily refresh
- add statistical forecasting for ticket volume
- add cost-to-serve by product and country
- add cohort analysis for repeat purchase impact
