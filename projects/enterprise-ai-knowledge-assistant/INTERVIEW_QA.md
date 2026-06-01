# Interview Q&A

## How would you explain this project?

I built a governed enterprise AI assistant prototype for a university-style organization. It retrieves approved department guidance, creates structured answers, applies safety guardrails, and runs evaluation tests before deployment. The goal is to show that enterprise AI requires knowledge management, prompt design, testing, monitoring, and rollback planning.

## Why did you use synthetic data?

Real HR, student services, IT, and academic policy documents are usually internal and sensitive. I created realistic sample policy notes so I could demonstrate the workflow without exposing private information.

## Is this a real RAG system?

It is a RAG-style prototype. It retrieves relevant passages from a knowledge base before drafting an answer. To keep the project free and explainable, I used keyword scoring instead of paid embeddings. In production, I would use embeddings and approved enterprise data sources.

## What makes this more than a chatbot?

The project includes guardrails, structured outputs, regression tests, department-specific behavior, knowledge base management, and an AI operations runbook. That reflects how enterprise AI has to be managed after launch.

## What safety issues did you consider?

I included guardrails for passwords, Social Security numbers, financial aid estimates, leave approvals, academic misconduct decisions, and other cases where the assistant should not make a formal decision.

## How would you improve it in a real company?

I would connect approved internal sources, add document metadata and owner approval dates, use embeddings, log feedback, monitor low-confidence answers, and add a human review workflow for sensitive cases.
