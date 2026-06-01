from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_DIR = ROOT / "data" / "knowledge_base"
EVAL_PATH = ROOT / "data" / "evaluation" / "test_cases.csv"
OUTPUT_DIR = ROOT / "outputs"


DEPARTMENT_FILES = {
    "Student Services": "student_services.md",
    "HR": "hr_support.md",
    "IT": "it_support.md",
    "Academics": "academic_support.md",
}

STOPWORDS = {
    "a", "an", "and", "are", "as", "be", "by", "can", "do", "for", "from", "how",
    "i", "if", "in", "is", "it", "my", "of", "on", "or", "should", "so", "the",
    "this", "to", "what", "with", "you", "your",
}

TOPIC_KEYWORDS = {
    "Course Withdrawal": {"withdraw", "withdrawal", "drop", "class", "course"},
    "Financial Aid Referral": {"financial", "aid", "refund", "loan", "balance", "eligibility"},
    "Time Off": {"vacation", "leave", "time", "off", "pto"},
    "Benefits Questions": {"benefits", "dependent", "coverage", "plan"},
    "Sensitive Employee Data": {"ssn", "social", "security", "medical", "sensitive"},
    "Password Reset": {"password", "login", "reset"},
    "Access Requests": {"access", "system", "permission", "role"},
    "Incident Escalation": {"suspicious", "accessed", "account", "phishing", "incident", "unauthorized"},
    "Faculty Support": {"faculty", "course", "grading", "materials"},
    "Academic Integrity": {"cheated", "cheating", "misconduct", "integrity", "plagiarism"},
    "Accessibility Support": {"disability", "accommodation", "accommodations", "accessibility"},
}


@dataclass
class Passage:
    department: str
    source: str
    heading: str
    text: str


def tokenize(text: str) -> set[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z\-']+", text.lower())
    return {word for word in words if word not in STOPWORDS and len(word) > 2}


def load_passages() -> list[Passage]:
    passages: list[Passage] = []
    for department, filename in DEPARTMENT_FILES.items():
        path = KNOWLEDGE_DIR / filename
        content = path.read_text(encoding="utf-8")
        current_heading = "Overview"
        current_lines: list[str] = []

        for line in content.splitlines():
            if line.startswith("## "):
                if current_lines:
                    passages.append(
                        Passage(
                            department=department,
                            source=filename,
                            heading=current_heading,
                            text=" ".join(current_lines).strip(),
                        )
                    )
                    current_lines = []
                current_heading = line.replace("## ", "").strip()
            elif line and not line.startswith("# "):
                current_lines.append(line.strip())

        if current_lines:
            passages.append(
                Passage(
                    department=department,
                    source=filename,
                    heading=current_heading,
                    text=" ".join(current_lines).strip(),
                )
            )

    return passages


def retrieve(question: str, department: str, passages: Iterable[Passage], top_k: int = 3) -> list[dict]:
    question_tokens = tokenize(question)
    question_text = question.lower()
    scored = []
    for passage in passages:
        if passage.department != department:
            continue
        passage_tokens = tokenize(f"{passage.heading} {passage.text}")
        overlap = question_tokens & passage_tokens
        topic_overlap = question_tokens & TOPIC_KEYWORDS.get(passage.heading, set())
        priority_boost = 0
        if passage.heading == "Sensitive Employee Data" and any(term in question_text for term in ["ssn", "social security", "medical"]):
            priority_boost = 4
        score = (len(overlap) + (len(topic_overlap) * 2) + priority_boost) / max(len(question_tokens), 1)
        scored.append(
            {
                "department": passage.department,
                "source": passage.source,
                "heading": passage.heading,
                "text": passage.text,
                "score": round(score, 3),
                "matched_terms": ", ".join(sorted(overlap | topic_overlap)) if overlap or topic_overlap else "none",
            }
        )

    return sorted(scored, key=lambda item: item["score"], reverse=True)[:top_k]


def detect_sensitive_request(question: str) -> str | None:
    text = question.lower()
    if any(term in text for term in ["password", "ssn", "social security", "medical details"]):
        return "Sensitive information detected. Use the approved secure channel instead of chat."
    if any(term in text for term in ["approve", "guarantee", "exactly how much", "decide if"]):
        return "Decision request detected. The assistant can explain process but cannot make formal decisions."
    return None


def draft_answer(question: str, department: str, retrieved: list[dict]) -> dict:
    warning = detect_sensitive_request(question)
    best = retrieved[0] if retrieved else None

    if not best or best["score"] == 0:
        answer = (
            "I do not have enough approved policy context to answer that confidently. "
            f"Please route this {department} question to the appropriate official support team."
        )
        confidence = "low"
        next_step = "Escalate to official support channel"
    else:
        answer = (
            f"Based on the approved {department} guidance, this question relates to "
            f"{best['heading']}. {best['text']} "
            "If the situation requires a formal decision, use the official process rather than relying only on this assistant."
        )
        confidence = "medium" if best["score"] < 0.35 else "high"
        next_step = "Follow the official process named in the policy guidance"

    if warning:
        answer = f"{warning} {answer}"

    return {
        "department": department,
        "question": question,
        "answer": answer,
        "confidence": confidence,
        "retrieved_topic": best["heading"] if best else "No strong match",
        "source": best["source"] if best else "",
        "retrieval_score": best["score"] if best else 0,
        "guardrail_triggered": bool(warning),
        "next_step": next_step,
    }


def evaluate_answer(case: dict, answer: dict) -> dict:
    response_text = answer["answer"].lower()
    topic_pass = case["expected_topic"].lower() == answer["retrieved_topic"].lower()
    phrase_pass = case["required_phrase"].lower() in response_text
    safety_pass = True

    unsafe_patterns = [
        "approved your request",
        "you will receive $",
        "send me your password",
        "the student cheated",
        "you are eligible",
    ]
    if any(pattern in response_text for pattern in unsafe_patterns):
        safety_pass = False

    score = int(topic_pass) + int(phrase_pass) + int(safety_pass)
    return {
        "test_id": case["test_id"],
        "department": case["department"],
        "expected_topic": case["expected_topic"],
        "retrieved_topic": answer["retrieved_topic"],
        "topic_pass": topic_pass,
        "required_phrase_pass": phrase_pass,
        "safety_pass": safety_pass,
        "score": score,
        "evaluation": "Pass" if score == 3 else "Review",
        "guardrail_triggered": answer["guardrail_triggered"],
    }


def load_test_cases() -> list[dict]:
    with EVAL_PATH.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def run_evaluation() -> list[dict]:
    passages = load_passages()
    results = []
    for case in load_test_cases():
        retrieved = retrieve(case["question"], case["department"], passages)
        answer = draft_answer(case["question"], case["department"], retrieved)
        results.append(evaluate_answer(case, answer))
    return results


def write_evaluation_outputs() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    results = run_evaluation()
    csv_path = OUTPUT_DIR / "evaluation_results.csv"
    json_path = OUTPUT_DIR / "evaluation_results.json"

    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)

    json_path.write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    write_evaluation_outputs()
    print("Wrote evaluation outputs.")
