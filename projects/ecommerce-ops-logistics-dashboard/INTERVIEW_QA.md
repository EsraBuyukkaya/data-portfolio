# Interview Q&A

## What problem does this project solve?

It helps an e-commerce operations team monitor fulfillment, logistics, returns, support tickets, SLA pressure, and backlog risk in one dashboard.

## Why did you use synthetic data?

Real 3PL, carrier, WMS, and CX exports are usually private. I created synthetic data that mirrors the structure and behavior of those data feeds so I could demonstrate the analytics workflow ethically.

## What makes this project relevant to operations analytics?

It connects operational metrics to business outcomes: late deliveries, return rates, shipping cost, ticket volume, SLA breaches, and cost to serve.

## What SQL skills does it show?

It includes queries for carrier performance, fulfillment-center reporting, CX ticket drivers, product return pressure, and backlog risk days.

## What would you do differently in a real company?

I would connect the dashboard to real operational data feeds, automate refresh, build data quality checks, and validate each metric against source systems.

## What is the backlog risk score?

It is a simple rules-based score using ticket volume, SLA breaches, and late delivery rate. It helps flag days that may need staffing review, proactive customer communication, or carrier follow-up.

## Is this machine learning?

No. It is intentionally a transparent rules-based prototype. In a production version, I would test whether a forecasting model improves ticket-volume or return-risk prediction.
