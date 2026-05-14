from __future__ import annotations

import csv
import random
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"


CUSTOMER_NAMES = [
    "Northstar Health",
    "Metro Auto Club",
    "BrightPath Education",
    "Summit Home Services",
    "Evergreen Retail",
    "Pioneer Insurance",
    "Cedar Finance",
    "Luma Wellness",
    "Atlas Travel",
    "Harbor Telecom",
]


def main() -> None:
    random.seed(7)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    customers = []
    launches = []
    calls = []
    blockers = []

    industries = ["Healthcare", "Insurance", "Education", "Retail", "Home Services", "Travel"]
    owners = ["Customer Strategy", "Forward Deployed Engineering", "Product", "Customer Success"]
    use_cases = ["support triage", "sales qualification", "appointment scheduling", "renewal reminder"]
    intents = ["pricing", "reschedule", "cancel", "technical issue", "eligibility", "purchase intent"]

    for idx, name in enumerate(CUSTOMER_NAMES, start=1):
        customer_id = f"C{idx:03d}"
        industry = random.choice(industries)
        contract_value = random.choice([125000, 220000, 350000, 500000, 750000])
        owner = random.choice(owners)
        customers.append(
            {
                "customer_id": customer_id,
                "customer_name": name,
                "industry": industry,
                "contract_value": contract_value,
                "launch_owner": owner,
            }
        )

        readiness = random.randint(48, 98)
        qa_pass = round(random.uniform(0.72, 0.99), 2)
        days_to_go_live = random.randint(1, 21)
        if readiness >= 85 and qa_pass >= 0.9:
            status = "On Track"
        elif readiness < 65 or qa_pass < 0.8:
            status = "At Risk"
        else:
            status = "Needs Attention"
        launches.append(
            {
                "customer_id": customer_id,
                "kickoff_day": random.randint(1, 14),
                "days_to_go_live": days_to_go_live,
                "readiness_score": readiness,
                "qa_pass_rate": qa_pass,
                "launch_status": status,
            }
        )

        for call_num in range(random.randint(120, 260)):
            use_case = random.choice(use_cases)
            contained_chance = {
                "support triage": 0.62,
                "sales qualification": 0.55,
                "appointment scheduling": 0.70,
                "renewal reminder": 0.67,
            }[use_case]
            contained = 1 if random.random() < contained_chance else 0
            escalated = 0 if contained else random.choice([0, 1])
            sentiment = round(random.uniform(2.5, 4.9) if contained else random.uniform(1.4, 3.4), 2)
            revenue = 0
            if use_case == "sales qualification" and contained:
                revenue = random.choice([0, 250, 500, 1000, 1500])
            calls.append(
                {
                    "call_id": f"{customer_id}-{call_num:04d}",
                    "customer_id": customer_id,
                    "agent_use_case": use_case,
                    "intent": random.choice(intents),
                    "contained": contained,
                    "escalated": escalated,
                    "customer_sentiment": sentiment,
                    "minutes_saved": random.randint(3, 12) if contained else random.randint(0, 4),
                    "revenue_influenced": revenue,
                }
            )

        blocker_count = random.randint(1, 5) if status != "On Track" else random.randint(0, 2)
        for blocker_num in range(blocker_count):
            blockers.append(
                {
                    "blocker_id": f"B{idx:03d}-{blocker_num + 1}",
                    "customer_id": customer_id,
                    "severity": random.choice(["Low", "Medium", "High", "Critical"]),
                    "status": random.choice(["Open", "In Progress", "Closed"]),
                    "owner": random.choice(owners),
                    "roadmap_category": random.choice(
                        ["Data integration", "Voice model", "Intent coverage", "Reporting", "Handoff workflow"]
                    ),
                    "blocker_summary": random.choice(
                        [
                            "Customer data mapping is incomplete.",
                            "Agent fails on a common customer intent.",
                            "Escalation handoff needs clearer routing.",
                            "Leadership wants clearer ROI reporting.",
                            "QA scripts need customer-specific examples.",
                        ]
                    ),
                }
            )

    write_csv(DATA_DIR / "customers.csv", customers)
    write_csv(DATA_DIR / "launches.csv", launches)
    write_csv(DATA_DIR / "agent_calls.csv", calls)
    write_csv(DATA_DIR / "blockers.csv", blockers)
    print(f"Created {len(customers)} customers, {len(launches)} launches, {len(calls)} calls, and {len(blockers)} blockers.")


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
