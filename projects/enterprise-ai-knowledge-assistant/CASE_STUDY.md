# Case Study: Enterprise AI Knowledge Assistant

## Business Problem

Enterprise AI assistants can improve service delivery, but they create risk if answers are inaccurate, off-policy, too casual, or based on outdated information. A university-style organization needs an assistant that can support multiple departments while staying aligned with approved institutional guidance.

## Users

- Student Services staff answering process questions
- HR staff supporting employees
- IT support teams handling access and security questions
- Academic teams answering process-oriented faculty questions
- AI governance or operations teams monitoring quality

## My Approach

1. Created synthetic approved policy notes for Student Services, HR, IT, and Academics.
2. Split the knowledge into retrievable passages by department and topic.
3. Built a lightweight retrieval function that scores passages against a user question.
4. Designed a structured assistant response with answer, confidence, source, topic, guardrail flag, and next step.
5. Added safety detection for sensitive information and formal decision requests.
6. Built regression test cases that evaluate topic match, required phrase, and safety behavior.
7. Documented an AI operations runbook for prompt changes, testing, monitoring, and rollback.

## Key Design Decisions

| Decision | Why It Matters |
|---|---|
| Synthetic policy notes | Avoids exposing private institutional documents |
| Structured outputs | Makes answers easier to log, inspect, and use in workflows |
| Safety guardrails | Reduces risk around passwords, SSNs, financial decisions, and misconduct decisions |
| Evaluation tests | Shows how prompt and retrieval changes can be tested before deployment |
| Runbook tab | Shows operational maturity beyond a basic chatbot demo |

## Business Impact

This kind of system could help an organization:

- reduce repeated support questions
- improve consistency across departments
- route sensitive questions to the correct human team
- test AI behavior before release
- document prompt and knowledge changes
- monitor quality over time

## Next Improvements

- connect to approved SharePoint or knowledge-base content
- add embedding-based retrieval
- store prompt versions and test results in a database
- add user feedback collection
- track fallback and low-confidence answer rates
- add human review queues for sensitive or uncertain answers
