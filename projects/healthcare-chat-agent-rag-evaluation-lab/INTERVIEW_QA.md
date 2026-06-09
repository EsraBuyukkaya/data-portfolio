# Interview Q&A

## How would you explain this project?

I built a local Python experiment lab for testing prompt changes in a healthcare chat-assistant workflow. It uses approved knowledge notes, retrieves relevant context for patient questions, compares a baseline prompt with a revised prompt, and scores both variants against regression tests for safety, escalation, required wording, and retrieval accuracy.

## Why did you build it this way?

The job description asked for evidence-backed prompt engineering, RAG comfort, regression coverage, and clear recommendations. I wanted the project to show that prompt changes should be tested systematically before they are shipped, especially in healthcare where unsafe or overconfident answers can create risk.

## Is this a real LLM?

No. This is a free local prototype. The retrieval and scoring are implemented in Python, and the answer behavior is deterministic so the experiment is repeatable. In production, the same harness could be connected to a real LLM, chatbot, or agent system.

## What did the experiment show?

The revised prompt improved overall pass rate from 58.3% to 91.7%. The biggest improvements were in safety and escalation behavior. Retrieval stayed the same across both variants, which helped isolate the prompt behavior from the knowledge base.

## What does this prove about your skills?

It shows that I understand prompt testing as an operations and evaluation problem, not just writing a clever prompt. I can create test cases, define expected behavior, run evaluations, compare variants, and communicate a recommendation clearly.

## What would you improve next?

I would add a larger test set, use real chat transcripts after removing protected information, add reviewer scoring, track prompt versions, and run statistical analysis to confirm whether improvements are significant.
