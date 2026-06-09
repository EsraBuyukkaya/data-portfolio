# Healthcare Chat Agent RAG Evaluation Lab

Scenario prototype for a healthcare AI team improving a patient support chat assistant.

## Scenario

A multi-location healthcare provider uses an AI chat assistant to answer routine patient questions. Before changing the global prompt, the AI team needs evidence that the new prompt improves retrieval, safety, escalation behavior, and patient-friendly tone without breaking existing workflows.

This project creates a local Python lab for testing prompt variants against healthcare chat scenarios.

## App Preview

![Healthcare chat RAG demo](assets/screenshots/healthcare-chat-rag-demo.png)

| Experiment Results | Regression Tests |
|---|---|
| ![Experiment results](assets/screenshots/healthcare-chat-rag-results.png) | ![Regression tests](assets/screenshots/healthcare-chat-rag-tests.png) |

![Knowledge base](assets/screenshots/healthcare-chat-rag-knowledge-base.png)

## What This Project Demonstrates

- Retrieval-augmented generation concepts using local policy documents
- Prompt variant testing with a baseline prompt and revised healthcare chat-assistant prompt
- Regression test cases across scheduling, billing, privacy, urgent symptoms, prescriptions, and portal support
- Evaluation metrics for retrieval match, required wording, escalation behavior, and safety
- Clear experiment recommendations that product and engineering teams can act on

## Why This Matters

Prompt changes can improve one workflow while quietly breaking another. This project treats prompt updates like experiments instead of guesses.

The workflow:

1. Loads approved healthcare support knowledge.
2. Chunks documents into retrievable passages.
3. Retrieves likely source context for each patient question.
4. Simulates answer behavior under two prompt variants.
5. Scores each response against regression-test expectations.
6. Produces a recommendation for whether the revised prompt is safer to ship.

## Results

| Metric | Baseline Prompt | Revised Prompt |
|---|---:|---:|
| Test cases | 12 | 12 |
| Retrieval pass rate | 91.7% | 91.7% |
| Required wording pass rate | 91.7% | 100.0% |
| Safety pass rate | 58.3% | 100.0% |
| Escalation pass rate | 58.3% | 100.0% |
| Overall pass rate | 58.3% | 91.7% |

The revised prompt performed better because it explicitly instructed the assistant to use approved context, avoid final medical/financial decisions, escalate urgent or protected situations, and maintain a concise patient-friendly chat tone.

## Project Files

| File | Purpose |
|---|---|
| `src/rag_eval.py` | Local RAG retrieval and prompt-regression evaluation script |
| `src/app.py` | Streamlit dashboard for reviewing experiment results |
| `data/knowledge_base/` | Approved healthcare support policy notes |
| `data/test_cases.csv` | Regression cases and expected behavior |
| `data/prompt_variants.csv` | Baseline and revised prompt instructions |
| `outputs/evaluation_results.csv` | Prompt-level test results |
| `outputs/experiment_summary.json` | Summary metrics |
| `CASE_STUDY.md` | Business case study |
| `INTERVIEW_QA.md` | Interview talking points |

## How To Run

```powershell
python src\rag_eval.py
python -m streamlit run src\app.py
```

## Skills Shown

- Python
- RAG concepts
- Prompt engineering
- Prompt regression testing
- Evaluation rubrics
- Healthcare AI guardrails
- Chat-agent workflow thinking
- Experiment design
- Product and engineering communication

## Limitations

This is a local portfolio prototype. It does not call a paid LLM API and does not process real patient data. The answer-generation behavior is deterministic so the experiment can run for free and produce repeatable results. In production, I would connect the same evaluation harness to live model outputs, chat transcripts, prompt versions, and statistical significance testing across larger samples.
