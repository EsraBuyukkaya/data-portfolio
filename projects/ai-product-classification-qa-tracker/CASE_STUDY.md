# Case Study: AI Product Classification QA Tracker

## Business Problem

Retail product-classification models process large volumes of records, but incorrect or ambiguous labels can damage catalog quality and downstream reporting. Human reviewers need consistent guidelines, a prioritized queue, and visibility into recurring failure patterns.

## Users

- AI Operations specialists reviewing model outputs
- catalog teams maintaining product categories
- analysts monitoring model quality
- operations leaders deciding where additional training data is needed

## My Approach

1. Created realistic retail product records with AI-predicted categories and confidence scores.
2. Defined a category guide that acts as a lightweight review SOP.
3. Added reviewer-approved labels, error reasons, statuses, and notes.
4. Built Apps Script rules that identify mismatches, low-confidence records, and research needs.
5. Created a high-priority review queue and quality dashboard.
6. Validated the same metrics independently with Python.

## Key Findings

- The model achieved 76.0% accuracy across completed reviews.
- Eleven category disagreements were identified: six were resolved in completed reviews and five remain in the research queue.
- Eleven records had confidence below 70%.
- Thirteen records required high-priority human attention.
- Ambiguity frequently appeared around supplements, plant-based items, and products that could fit similar categories.

## Recommended Actions

- Add more labeled training examples for Health and Wellness products.
- Review category coverage when products require a missing category such as Pet Care.
- Evaluate low-confidence and mismatch records before adding them to the production catalog.
- Track error patterns by model version and product segment.
- Use two reviewers for difficult records and measure agreement.

## Why This Matters

The project shows that AI Operations is not only about accepting or rejecting predictions. It requires clear review rules, careful research, consistent annotations, quality measurement, and feedback that can improve future model performance.
