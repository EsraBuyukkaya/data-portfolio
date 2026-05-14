from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"


def main() -> None:
    random.seed(24)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    patients = build_patients()
    encounters = build_encounters(patients)
    conditions = build_conditions(encounters)
    observations = build_observations(encounters)

    write_csv(RAW_DIR / "patients.csv", patients)
    write_csv(RAW_DIR / "encounters.csv", encounters)
    write_csv(RAW_DIR / "conditions.csv", conditions)
    write_csv(RAW_DIR / "observations.csv", observations)
    print(
        "Created raw healthcare files: "
        f"{len(patients)} patients, {len(encounters)} encounters, "
        f"{len(conditions)} conditions, {len(observations)} observations."
    )


def build_patients() -> list[dict]:
    cities = ["Albany", "Buffalo", "Rochester", "Syracuse", "Yonkers"]
    genders = ["F", "M"]
    patients = []
    for idx in range(1, 151):
        birth_year = random.randint(1942, 2018)
        birth_date = date(birth_year, random.randint(1, 12), random.randint(1, 28))
        patients.append(
            {
                "patient_id": f"P{idx:04d}",
                "birth_date": birth_date.isoformat(),
                "gender": random.choice(genders),
                "city": random.choice(cities),
                "state": "NY",
            }
        )

    patients.append(patients[10].copy())  # duplicate patient ID
    patients.append(
        {
            "patient_id": "",
            "birth_date": "2035-01-01",
            "gender": "F",
            "city": "Albany",
            "state": "NY",
        }
    )
    return patients


def build_encounters(patients: list[dict]) -> list[dict]:
    classes = ["ambulatory", "emergency", "inpatient", "wellness", "urgentcare"]
    encounters = []
    real_patients = [p["patient_id"] for p in patients if p["patient_id"]]
    encounter_id = 1
    for patient_id in real_patients[:150]:
        for _ in range(random.randint(1, 4)):
            start = date(2024, 1, 1) + timedelta(days=random.randint(0, 360))
            stop = start + timedelta(hours=random.randint(1, 96) // 24)
            encounters.append(
                {
                    "encounter_id": f"E{encounter_id:05d}",
                    "patient_id": patient_id,
                    "start_date": start.isoformat(),
                    "stop_date": stop.isoformat(),
                    "encounter_class": random.choice(classes),
                    "organization": random.choice(["Healthix North", "Healthix Central", "Healthix South"]),
                }
            )
            encounter_id += 1

    encounters.append(
        {
            "encounter_id": f"E{encounter_id:05d}",
            "patient_id": "P9999",
            "start_date": "2024-06-01",
            "stop_date": "2024-06-01",
            "encounter_class": "emergency",
            "organization": "Healthix North",
        }
    )
    encounter_id += 1
    encounters.append(
        {
            "encounter_id": f"E{encounter_id:05d}",
            "patient_id": "P0001",
            "start_date": "2024-08-20",
            "stop_date": "2024-08-18",
            "encounter_class": "inpatient",
            "organization": "Healthix Central",
        }
    )
    return encounters


def build_conditions(encounters: list[dict]) -> list[dict]:
    condition_options = [
        ("44054006", "Diabetes mellitus"),
        ("38341003", "Hypertension"),
        ("195967001", "Asthma"),
        ("73211009", "Diabetes mellitus type 2"),
        ("55822004", "Hyperlipidemia"),
    ]
    rows = []
    for encounter in encounters:
        if random.random() < 0.56:
            code, description = random.choice(condition_options)
            rows.append(
                {
                    "condition_id": f"C{len(rows) + 1:05d}",
                    "patient_id": encounter["patient_id"],
                    "encounter_id": encounter["encounter_id"],
                    "start_date": encounter["start_date"],
                    "code": code,
                    "description": description,
                }
            )
    return rows


def build_observations(encounters: list[dict]) -> list[dict]:
    observation_options = [
        ("8480-6", "Systolic Blood Pressure", "mmHg", 90, 180),
        ("39156-5", "Body Mass Index", "kg/m2", 18, 42),
        ("4548-4", "Hemoglobin A1c", "%", 4, 12),
    ]
    rows = []
    for encounter in encounters:
        for code, description, unit, low, high in observation_options:
            rows.append(
                {
                    "observation_id": f"O{len(rows) + 1:05d}",
                    "patient_id": encounter["patient_id"],
                    "encounter_id": encounter["encounter_id"],
                    "date": encounter["start_date"],
                    "code": code,
                    "description": description,
                    "value": round(random.uniform(low, high), 1),
                    "unit": unit,
                }
            )

    rows.append(
        {
            "observation_id": f"O{len(rows) + 1:05d}",
            "patient_id": "P0001",
            "encounter_id": "E99999",
            "date": "2024-03-01",
            "code": "8480-6",
            "description": "Systolic Blood Pressure",
            "value": 350,
            "unit": "mmHg",
        }
    )
    rows.append(
        {
            "observation_id": f"O{len(rows) + 1:05d}",
            "patient_id": "P0002",
            "encounter_id": "E00002",
            "date": "2024-03-01",
            "code": "39156-5",
            "description": "Body Mass Index",
            "value": -1,
            "unit": "kg/m2",
        }
    )
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
