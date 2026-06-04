# Interview Q&A

## How would you explain this project?

I built a Google Sheets and Apps Script workflow for reviewing AI-generated retail product classifications. It compares AI predictions with reviewer-approved labels, prioritizes low-confidence and ambiguous cases, and summarizes accuracy and recurring quality issues.

## Why is this relevant to AI Operations?

AI systems need ongoing human evaluation. This project demonstrates model-output review, data annotation, ambiguous-case research, quality scoring, and a feedback workflow that helps identify where a model needs improvement.

## How did you decide which records were high priority?

A record is high priority if it needs research, does not have an approved reviewer label, disagrees with the reviewer, or has AI confidence below 70%. The rules are documented so different reviewers can follow the same process.

## What did Apps Script automate?

Apps Script adds a custom menu, recalculates quality flags, highlights priority records, timestamps completed reviews, assigns the next high-priority item, and generates a QA dashboard.

## Why use Google Sheets?

Google Sheets is accessible to operations teams, supports collaboration, and is often used for lightweight review workflows. Apps Script adds automation without requiring a paid platform.

## What did you learn from the sample data?

The reviewed model accuracy was 76%. The most difficult classifications involved supplements, plant-based frozen items, and products that could fit similar categories. That indicates where better category guidance or additional training examples would help.

## How would you improve this in production?

I would connect model outputs through an API, track reviewer identity, measure agreement between reviewers, version the category guide, record model versions, and send completed annotations back into a governed training-data pipeline.
