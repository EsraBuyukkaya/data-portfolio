# Case Study: Healthcare Chat Agent RAG Evaluation Lab

## Business Problem

A healthcare chat assistant handles patient questions for routine workflows such as appointment scheduling, billing, prescription questions, portal support, and general location information.

The team wants to improve the global prompt, but prompt changes are risky. A better tone in one workflow could create unsafe behavior in another, especially when patients ask about urgent symptoms, privacy, billing, or medication instructions.

## Goal

Build a local experiment lab that evaluates prompt variants before a change is shipped.

## Approach

1. Created approved healthcare knowledge notes for scheduling, billing, privacy, prescription support, urgent symptoms, and portal access.
2. Built a simple local retrieval system in Python to match patient questions to relevant approved context.
3. Defined two prompt variants: a baseline prompt and a revised healthcare chat prompt.
4. Created regression test cases with expected topics, required phrases, escalation requirements, and safety expectations.
5. Scored each prompt variant across retrieval, wording, safety, escalation, and overall pass/fail behavior.

## Key Findings

- The revised prompt improved overall pass rate from 58.3% to 91.7%.
- Required wording pass rate improved from 91.7% to 100.0%.
- Safety pass rate improved from 58.3% to 100.0%.
- Escalation pass rate improved from 58.3% to 100.0%.
- Retrieval performance stayed the same, which means the improvement came from prompt behavior, not a different knowledge base.

## Recommendation

Ship the revised prompt only after expanding the regression suite with more real chat categories and running a larger experiment. The current results support moving the revised prompt into a controlled pilot because it improves safety and required workflow language without reducing retrieval quality.

## What I Would Add In Production

- Live LLM outputs for each prompt version
- Chat transcript sampling
- Chat reviewer agreement tracking
- Confidence intervals and significance tests
- Prompt version history
- Regression monitoring after deployment
- Rollback criteria if safety or escalation scores drop
