-- Product analytics queries for the Healthcare Member Engagement AI project.
-- These queries are written for SQLite.

-- 1. Member engagement overview
SELECT
  COUNT(*) AS total_members,
  ROUND(AVG(app_sessions_30d), 1) AS avg_app_sessions_30d,
  ROUND(AVG(CASE WHEN renewal_due_days <= 30 THEN 1 ELSE 0 END), 3) AS renewal_due_30d_rate,
  ROUND(AVG(CASE WHEN missed_appointment_90d = 1 THEN 1 ELSE 0 END), 3) AS missed_appointment_rate
FROM members;

-- 2. Engagement risk by plan type
SELECT
  plan_type,
  COUNT(*) AS members,
  ROUND(AVG(risk_score), 3) AS avg_risk_score,
  SUM(CASE WHEN risk_score >= 70 THEN 1 ELSE 0 END) AS high_risk_members
FROM members
GROUP BY plan_type
ORDER BY avg_risk_score DESC;

-- 3. Outreach response by channel
SELECT
  channel,
  COUNT(*) AS messages_sent,
  SUM(CASE WHEN responded = 1 THEN 1 ELSE 0 END) AS responses,
  ROUND(AVG(responded), 3) AS response_rate
FROM outreach
GROUP BY channel
ORDER BY response_rate DESC;

-- 4. Members needing product or operations follow-up
SELECT
  member_id,
  plan_type,
  phone_reliability,
  app_sessions_30d,
  renewal_due_days,
  support_tickets_30d,
  missed_appointment_90d,
  risk_score
FROM members
WHERE risk_score >= 70
ORDER BY risk_score DESC
LIMIT 25;

-- 5. Window-function example: rank highest-risk members inside each plan type
SELECT
  member_id,
  plan_type,
  risk_score,
  RANK() OVER (PARTITION BY plan_type ORDER BY risk_score DESC) AS risk_rank_in_plan
FROM members
ORDER BY plan_type, risk_rank_in_plan
LIMIT 30;
