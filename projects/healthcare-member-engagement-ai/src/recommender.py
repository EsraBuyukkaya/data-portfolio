from __future__ import annotations


def recommend_next_action(member: dict) -> tuple[str, str]:
    if int(member["renewal_due_days"]) <= 30 and int(member["app_sessions_30d"]) < 5:
        return (
            "Send renewal reminder",
            "Coverage renewal is due soon and recent app engagement is low.",
        )
    if int(member["missed_appointment_90d"]) == 1:
        return (
            "Offer scheduling support",
            "Member missed a recent appointment and may need help reconnecting to care.",
        )
    if int(member["support_tickets_30d"]) >= 2:
        return (
            "Route to support follow-up",
            "Multiple recent support tickets suggest friction in the member experience.",
        )
    if str(member["phone_reliability"]) == "low":
        return (
            "Use app notification plus backup call",
            "Phone reliability is low, so outreach should not rely on one channel.",
        )
    return (
        "Continue standard engagement",
        "No urgent risk trigger was found based on the current rules.",
    )
