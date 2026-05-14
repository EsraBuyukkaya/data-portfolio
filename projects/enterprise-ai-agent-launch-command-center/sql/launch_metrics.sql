-- Launch and AI agent metrics for the Enterprise AI Agent Launch Command Center.
-- These queries are written for SQLite.

-- 0. Real public outreach/contact performance from UCI Bank Marketing
SELECT
  job,
  contact,
  COUNT(*) AS contacts,
  ROUND(AVG(converted_flag), 3) AS conversion_rate,
  ROUND(AVG(call_duration_seconds), 1) AS avg_call_duration_seconds,
  ROUND(AVG(campaign_contacts), 1) AS avg_campaign_contacts
FROM bank_marketing_contacts
GROUP BY job, contact
HAVING contacts >= 100
ORDER BY conversion_rate DESC;

-- 1. Launch health by customer
SELECT
  c.customer_name,
  c.industry,
  l.launch_status,
  l.readiness_score,
  l.qa_pass_rate,
  l.days_to_go_live,
  COUNT(b.blocker_id) AS open_blockers
FROM launches l
JOIN customers c ON c.customer_id = l.customer_id
LEFT JOIN blockers b
  ON b.customer_id = l.customer_id
  AND b.status != 'Closed'
GROUP BY c.customer_name, c.industry, l.launch_status, l.readiness_score, l.qa_pass_rate, l.days_to_go_live
ORDER BY l.readiness_score ASC;

-- 2. AI agent performance by use case
SELECT
  agent_use_case,
  COUNT(*) AS calls,
  ROUND(AVG(contained), 3) AS containment_rate,
  ROUND(AVG(escalated), 3) AS escalation_rate,
  ROUND(AVG(customer_sentiment), 2) AS avg_sentiment,
  ROUND(SUM(revenue_influenced), 0) AS revenue_influenced
FROM agent_calls
GROUP BY agent_use_case
ORDER BY revenue_influenced DESC;

-- 3. Customers with highest measurable business impact
SELECT
  c.customer_name,
  c.industry,
  COUNT(a.call_id) AS calls,
  ROUND(AVG(a.contained), 3) AS containment_rate,
  ROUND(SUM(a.minutes_saved), 0) AS minutes_saved,
  ROUND(SUM(a.revenue_influenced), 0) AS revenue_influenced
FROM customers c
JOIN agent_calls a ON a.customer_id = c.customer_id
GROUP BY c.customer_name, c.industry
ORDER BY revenue_influenced DESC;

-- 4. Roadmap feedback themes from blockers
SELECT
  roadmap_category,
  severity,
  COUNT(*) AS blocker_count
FROM blockers
WHERE status != 'Closed'
GROUP BY roadmap_category, severity
ORDER BY blocker_count DESC;

-- 5. Window-function example: rank customer launches by risk inside each launch status
SELECT
  customer_name,
  launch_status,
  readiness_score,
  qa_pass_rate,
  RANK() OVER (PARTITION BY launch_status ORDER BY readiness_score ASC, qa_pass_rate ASC) AS risk_rank
FROM launches
JOIN customers USING (customer_id)
ORDER BY launch_status, risk_rank;
