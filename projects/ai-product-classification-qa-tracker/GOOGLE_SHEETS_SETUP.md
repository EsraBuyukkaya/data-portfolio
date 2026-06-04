# Google Sheets Setup Guide

This guide lets you reproduce the project in a free Google account.

## Part 1: Create the Workbook

1. Open [Google Sheets](https://sheets.google.com).
2. Create a blank spreadsheet.
3. Rename it `AI Product Classification QA Tracker`.
4. Import `data/sample_product_evaluations.csv` and choose **Insert new sheet(s)**.
5. Import `data/category_guide.csv` and choose **Insert new sheet(s)**.

The setup automation recognizes the imported tab names and safely renames them to `Evaluations` and `Category Guide`. Choosing **Insert new sheet(s)** prevents an import from replacing existing project data.

## Part 2: Add the Apps Script

1. In the spreadsheet, select **Extensions > Apps Script**.
2. Delete the starter `myFunction` code.
3. Copy all code from `apps-script/Code.gs`.
4. Paste it into the Apps Script editor.
5. Save the project as `AI Product Classification QA Tracker`.
6. Return to the spreadsheet and refresh the browser tab.

Google will ask for permission the first time you run the script because it edits your spreadsheet.

## Part 3: Run the Workflow

1. Open the new **AI QA Tools** menu.
2. Select **Set up workbook**. This safely finds and renames the imported CSV tabs.
3. Select **Recalculate QA flags**.
4. Select **Refresh QA dashboard**.
5. Open the `QA Dashboard` tab.

The Evaluations tab will now contain:

- `category_match`
- `priority`
- `reviewed_at`

Rows will be highlighted:

- red for high-priority review
- yellow for medium-priority review
- green for accepted category matches

## Part 4: Demonstrate the Automation

To show that the workflow is interactive:

1. Find a record marked `Needs Research`.
2. Use the Category Guide to choose an approved category.
3. Update `reviewer_approved_category`.
4. Change `review_status` to `Reviewed`.
5. Notice that the match, priority, timestamp, and row color update.
6. Refresh the QA Dashboard to update the metrics.

## Recommended Screenshots

Save these for LinkedIn and GitHub:

1. `ai-qa-review-queue.png`: Evaluations tab showing highlighted priorities.
2. `ai-qa-dashboard.png`: QA Dashboard showing metrics and high-priority queue.
3. `ai-qa-category-guide.png`: Category Guide tab.
