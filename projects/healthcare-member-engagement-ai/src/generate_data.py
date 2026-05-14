from __future__ import annotations

import csv
import random
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"


def weighted_choice(options: list[tuple[str, float]]) -> str:
    values, weights = zip(*options)
    return random.choices(values, weights=weights, k=1)[0]


def calculate_risk(row: dict[str, int | str]) -> int:
    risk = 10
    risk += max(0, 8 - int(row["app_sessions_30d"])) * 4
    risk += 25 if int(row["missed_appointment_90d"]) else 0
    risk += 20 if int(row["renewal_due_days"]) <= 30 else 0
    risk += int(row["support_tickets_30d"]) * 6
    risk += {"high": 0, "medium": 10, "low": 22}[str(row["phone_reliability"])]
    return min(risk, 100)


def main() -> None:
    random.seed(42)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    members: list[dict[str, int | str]] = []
    events: list[dict[str, int | str]] = []
    outreach: list[dict[str, int | str]] = []

    plan_types = [("Medicaid", 0.58), ("Medicare Advantage", 0.28), ("Dual Eligible", 0.14)]
    reliability = [("high", 0.46), ("medium", 0.38), ("low", 0.16)]
    channels = ["sms", "phone_call", "app_notification"]

    for i in range(1, 301):
        member_id = f"M{i:04d}"
        phone_reliability = weighted_choice(reliability)
        app_sessions = max(0, int(random.gauss(9, 5)))
        renewal_due_days = random.randint(1, 120)
        support_tickets = random.choices([0, 1, 2, 3, 4], weights=[55, 25, 12, 6, 2], k=1)[0]
        missed_appt = 1 if random.random() < (0.12 if phone_reliability == "high" else 0.25) else 0

        row: dict[str, int | str] = {
            "member_id": member_id,
            "plan_type": weighted_choice(plan_types),
            "age_band": weighted_choice([("18-34", 0.22), ("35-49", 0.25), ("50-64", 0.30), ("65+", 0.23)]),
            "phone_reliability": phone_reliability,
            "app_sessions_30d": app_sessions,
            "renewal_due_days": renewal_due_days,
            "support_tickets_30d": support_tickets,
            "missed_appointment_90d": missed_appt,
        }
        row["risk_score"] = calculate_risk(row)
        members.append(row)

        for event_type in ["app_session", "benefit_view", "appointment", "support_ticket"]:
            count = {
                "app_session": app_sessions,
                "benefit_view": random.randint(0, 5),
                "appointment": random.randint(0, 2),
                "support_ticket": support_tickets,
            }[event_type]
            for _ in range(count):
                events.append(
                    {
                        "member_id": member_id,
                        "event_type": event_type,
                        "days_ago": random.randint(0, 90),
                    }
                )

        selected_channel = random.choice(channels)
        response_chance = {"sms": 0.34, "phone_call": 0.28, "app_notification": 0.41}[selected_channel]
        if phone_reliability == "low" and selected_channel in {"sms", "phone_call"}:
            response_chance -= 0.12
        outreach.append(
            {
                "member_id": member_id,
                "channel": selected_channel,
                "message_type": random.choice(["renewal", "appointment", "benefits", "support"]),
                "responded": 1 if random.random() < response_chance else 0,
            }
        )

    write_csv(DATA_DIR / "synthetic_members.csv", members)
    write_csv(DATA_DIR / "synthetic_events.csv", events)
    write_csv(DATA_DIR / "synthetic_outreach.csv", outreach)
    print(f"Created {len(members)} members, {len(events)} events, and {len(outreach)} outreach rows.")


def write_csv(path: Path, rows: list[dict[str, int | str]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
