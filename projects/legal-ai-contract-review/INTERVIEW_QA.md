# Interview Q&A: Legal AI Contract Review Assistant

## How would you describe this project?

This is a portfolio prototype for AI-assisted contract review. I built it from a legal innovation job-description scenario where a legal operations team wants to test whether a low-cost tool can extract important clauses, flag missing terms, and compare selected results against expert-labeled public data.

## What problem does it solve?

Legal teams often need to review contracts for important clauses such as governing law, termination, confidentiality, indemnification, and limitation of liability. This project shows a first-pass workflow that helps organize that review and identify where a human reviewer should look more closely.

## Why did you choose CUAD?

I chose CUAD because it is a public contract review dataset created for legal NLP research. It includes commercial contracts and expert-labeled clause data, which allowed me to test the prototype against an answer key instead of only showing a demo.

## What does the Streamlit app do?

The app lets a reviewer select a contract, see clause status counts, review extracted clauses, inspect the original contract text, and view evaluation results against CUAD labels when an answer key is available.

## Is this legal advice?

No. This is a portfolio prototype and first-pass review tool. It is designed to support review, not replace a lawyer. The app clearly treats the output as something that still needs human validation.

## What technologies did you use?

- Python
- Streamlit
- Regular expressions and rule-based text extraction
- JSON outputs
- Markdown reports
- CUAD public contract data
- GitHub for documentation and version control

## Why did you start with rule-based extraction instead of a large AI model?

I wanted the first version to be free, transparent, and easy to evaluate. A rule-based baseline makes it clear why the tool finds or misses something. That also made it easier to identify limitations before adding more advanced methods like embeddings, RAG, or LLM-based extraction.

## How did you evaluate the project?

I used selected labels from CUAD's `master_clauses.csv` as an answer key. The project compares the tool's extracted results against expected labels for selected clauses.

Current scored results:

| Contract | Scored Result |
|---|---|
| ABILITYINC Services Agreement | 3 of 3 |
| Conformis Development Agreement | 2 of 3 |
| Cerence Intellectual Property Agreement | 3 of 3 |

## Why is one result 2 of 3 instead of perfect?

The Conformis contract showed an important limitation. CUAD scores "Termination For Convenience" specifically, while my current detector looks for broader termination language. This mismatch is useful because it shows that legal AI tools need precise label definitions, not only keyword matching.

## What did you learn from building this?

I learned that legal documents often reuse similar terms across different sections. A simple keyword search can find the right word in the wrong legal context. That is why validation, clear label definitions, and human review matter in legal AI workflows.

## What would you improve next?

I would improve the project by:

- adding more CUAD contracts,
- separating general termination from termination for convenience,
- adding reviewer feedback fields,
- improving clause definitions,
- testing semantic matching with open-source embeddings,
- and later comparing the rule-based baseline with a RAG or LLM-assisted version.

## How does this relate to the job description?

The project maps directly to legal innovation and AI adoption responsibilities:

| Job Description Skill | Project Evidence |
|---|---|
| Contract review | Extracts and organizes key contract clauses |
| Clause extraction | Finds five target clause types |
| Document summarization | Produces first-pass review summaries and reports |
| AI workflow automation | Turns contract text into structured review output |
| Testing and validation | Compares selected results against CUAD expert labels |
| Feedback loops | Documents where human review and future feedback would improve the tool |
| Adoption planning | Includes a scenario, case study, app demo, and evaluation notes |

## How would you explain your use of AI tools while building this?

I used AI tools as a coding and learning assistant, but I made the project decisions, reviewed the outputs, tested the workflow, selected the dataset, and documented the limitations. I can explain how the project works and what I would improve next.

## What is the main takeaway?

This project shows that I can take a job-description requirement, turn it into a realistic scenario, build a working prototype, evaluate it against public data, and explain the results clearly.
