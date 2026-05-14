-- Healthcare ETL data quality and analytics queries.
-- These queries are written for SQLite.

-- 1. Duplicate patient IDs
SELECT
  patient_id,
  COUNT(*) AS duplicate_count
FROM raw_patients
GROUP BY patient_id
HAVING COUNT(*) > 1;

-- 2. Orphan encounters
SELECT
  e.encounter_id,
  e.patient_id
FROM raw_encounters e
LEFT JOIN raw_patients p ON p.patient_id = e.patient_id
WHERE p.patient_id IS NULL;

-- 3. Invalid encounter dates
SELECT
  encounter_id,
  patient_id,
  start_date,
  stop_date
FROM raw_encounters
WHERE DATE(stop_date) < DATE(start_date);

-- 4. Orphan observations
SELECT
  o.observation_id,
  o.encounter_id,
  o.patient_id
FROM raw_observations o
LEFT JOIN raw_encounters e ON e.encounter_id = o.encounter_id
WHERE e.encounter_id IS NULL;

-- 5. Out-of-range observations
SELECT
  observation_id,
  description,
  value,
  unit
FROM raw_observations
WHERE
  (description = 'Systolic Blood Pressure' AND (value < 60 OR value > 240))
  OR (description = 'Body Mass Index' AND (value < 10 OR value > 80))
  OR (description = 'Hemoglobin A1c' AND (value < 3 OR value > 20));

-- 6. Encounters by class
SELECT
  encounter_class,
  COUNT(*) AS encounters
FROM fact_encounter
GROUP BY encounter_class
ORDER BY encounters DESC;

-- 7. Top conditions
SELECT
  condition_description,
  COUNT(*) AS condition_count
FROM fact_condition
GROUP BY condition_description
ORDER BY condition_count DESC;

-- 8. Window-function example: patient encounter sequence
SELECT
  patient_id,
  encounter_id,
  start_date,
  ROW_NUMBER() OVER (PARTITION BY patient_id ORDER BY start_date) AS encounter_number
FROM fact_encounter
ORDER BY patient_id, encounter_number;
