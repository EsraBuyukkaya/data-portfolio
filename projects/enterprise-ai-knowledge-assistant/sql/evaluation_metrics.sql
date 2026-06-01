-- Evaluation summary for the Enterprise AI Knowledge Assistant.
-- These queries assume evaluation_results.csv has been loaded into a table
-- named evaluation_results.

SELECT
    COUNT(*) AS total_tests,
    SUM(CASE WHEN evaluation = 'Pass' THEN 1 ELSE 0 END) AS passed_tests,
    ROUND(100.0 * SUM(CASE WHEN evaluation = 'Pass' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pass_rate
FROM evaluation_results;

SELECT
    department,
    COUNT(*) AS tests,
    SUM(CASE WHEN evaluation = 'Pass' THEN 1 ELSE 0 END) AS passed_tests,
    SUM(CASE WHEN guardrail_triggered = 1 THEN 1 ELSE 0 END) AS guardrail_triggers
FROM evaluation_results
GROUP BY department
ORDER BY department;

SELECT
    test_id,
    department,
    expected_topic,
    retrieved_topic,
    topic_pass,
    required_phrase_pass,
    safety_pass,
    evaluation
FROM evaluation_results
WHERE evaluation <> 'Pass';
