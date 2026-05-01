# Case Study: Legal AI Contract Review Assistant

## Scenario

A legal operations team is exploring whether AI-assisted contract review could help lawyers and paralegals review routine commercial agreements faster.

The team does not want to adopt a tool blindly. Before investing in a vendor or larger AI system, they need a small prototype that can:

- review public sample contracts,
- extract key contract clauses,
- flag missing clauses,
- compare results against expert-labeled data,
- and show where the workflow still needs human review.

## Project Outcome

I built a free, local prototype that reviews contract text files and produces structured clause review reports.

The first version focuses on five clause types:

- Governing Law
- Termination
- Confidentiality
- Indemnification
- Limitation of Liability

The project uses CUAD, a public legal contract dataset from The Atticus Project, as the real-data source for sample contracts and expert labels.

## Why This Project Matters

The job description that inspired this project asked for experience with AI-powered legal technologies, contract review, clause extraction, workflow automation, user feedback, testing, validation, and adoption planning.

This project turns those requirements into a working portfolio deliverable.

## Data Source

Dataset: CUAD, The Contract Understanding Atticus Dataset

CUAD includes:

- 510 public commercial contracts,
- more than 13,000 expert clause labels,
- 41 legal clause categories,
- full contract text files,
- PDFs,
- and a master clauses CSV used as an answer key.

For this project, I started with a small sample instead of trying to process the entire dataset at once. This made it easier to build, test, and explain the workflow.

## Approach

I started with a rule-based baseline because it is transparent and easy to validate. The extractor looks for clause headings and keywords in contract sections, then produces:

- a clause checklist,
- extracted clause text,
- a plain-English summary,
- JSON results,
- and a Markdown review report.

After testing on the first real CUAD contract, I found that simple keyword matching could grab the wrong section when legal terms appeared in multiple places. For example, a section about termination may mention confidential information. I improved the extractor so it prioritizes clause headings before searching the full body text.

## Evaluation

The project compares extracted results against a small answer key derived from CUAD's expert-labeled `master_clauses.csv`.

Current evaluation sample:

| Contract | Source | Evaluation Status |
|---|---|---|
| ABILITYINC Services Agreement | CUAD | 3 of 3 scored labels passed |
| Conformis Development Agreement | CUAD | 2 of 3 scored labels passed |
| Cerence Intellectual Property Agreement | CUAD | 3 of 3 scored labels passed |

Some project clause types are not scored yet because CUAD does not include direct master-label columns for every clause I want the tool to identify. For example, the tool extracts Confidentiality and Indemnification sections, but the current CUAD master labels do not include general columns for those two categories.

One evaluation mismatch came from a label-definition difference. CUAD scores "Termination For Convenience" specifically, while the current project detector looks for broader termination language. This is a useful next improvement because it shows why legal AI tools need precise label definitions, not just keyword matches.

## Current Result

The current prototype can:

- read contract `.txt` files,
- extract target clauses,
- flag a missing Limitation of Liability clause,
- save structured JSON output,
- generate a readable Markdown report,
- and compare selected results against CUAD labels.

It also includes a small Streamlit demo app so the review workflow can be explored visually.

## What I Learned

Legal documents often use overlapping language. A term can appear in one clause even when that section is not the main clause being reviewed. This means legal AI tools need validation, human review, and careful evaluation logic.

The project also showed why a small baseline is useful before adding more advanced AI. Starting simple made it easier to see where the logic worked and where it failed.

## Next Iterations

- Add more CUAD contracts to the evaluation sample.
- Expand clause coverage.
- Add feedback fields for reviewer comments.
- Explore semantic matching with open-source embeddings.
- Later, compare rule-based extraction with an LLM or RAG workflow.
