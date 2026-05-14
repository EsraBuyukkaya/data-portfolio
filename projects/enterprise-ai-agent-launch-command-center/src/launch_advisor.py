from __future__ import annotations


def recommend_launch_action(row: dict) -> tuple[str, str]:
    readiness = int(row["readiness_score"])
    qa_pass_rate = float(row["qa_pass_rate"])
    days_to_go_live = int(row["days_to_go_live"])
    open_blockers = int(row.get("open_blockers", 0))
    containment_rate = float(row.get("containment_rate", 0))

    if readiness < 65 and days_to_go_live <= 7:
        return "Escalate launch risk", "Readiness is low and the go-live date is close."
    if qa_pass_rate < 0.80:
        return "Prioritize QA and prompt review", "QA pass rate is below the launch threshold."
    if open_blockers >= 2:
        return "Run blocker standup", "Multiple open blockers need owner-level follow-up."
    if containment_rate < 0.55:
        return "Review intents and handoff design", "Agent containment is below target."
    if readiness >= 85 and containment_rate >= 0.65:
        return "Prepare expansion proposal", "Launch health and agent performance are strong."
    return "Continue launch monitoring", "Launch is moving, but should stay under routine review."
