-- E-Commerce Operations & Logistics Dashboard
-- SQL examples for operational reporting and validation.

-- 1. Carrier performance
SELECT
    carrier,
    COUNT(*) AS orders,
    ROUND(AVG(delivery_days), 1) AS avg_delivery_days,
    ROUND(AVG(CASE WHEN late_delivery = 1 THEN 1.0 ELSE 0 END) * 100, 1) AS late_delivery_rate,
    ROUND(AVG(shipping_cost), 2) AS avg_shipping_cost
FROM orders
GROUP BY carrier
ORDER BY late_delivery_rate DESC;

-- 2. Fulfillment center performance
SELECT
    fulfillment_center,
    COUNT(*) AS orders,
    ROUND(AVG(CASE WHEN late_delivery = 1 THEN 1.0 ELSE 0 END) * 100, 1) AS late_delivery_rate,
    ROUND(AVG(CASE WHEN returned = 1 THEN 1.0 ELSE 0 END) * 100, 1) AS return_rate
FROM orders
GROUP BY fulfillment_center
ORDER BY late_delivery_rate DESC;

-- 3. CX ticket drivers
SELECT
    category,
    channel,
    COUNT(*) AS tickets,
    ROUND(AVG(first_response_hours), 1) AS avg_first_response_hours,
    ROUND(AVG(CASE WHEN sla_breached = 1 THEN 1.0 ELSE 0 END) * 100, 1) AS sla_breach_rate
FROM support_tickets
GROUP BY category, channel
ORDER BY tickets DESC;

-- 4. Product return pressure
SELECT
    product_line,
    COUNT(*) AS orders,
    ROUND(SUM(order_value), 0) AS revenue,
    ROUND(AVG(CASE WHEN returned = 1 THEN 1.0 ELSE 0 END) * 100, 1) AS return_rate
FROM orders
GROUP BY product_line
ORDER BY return_rate DESC;

-- 5. Backlog risk days
SELECT
    order_date,
    orders,
    tickets,
    sla_breaches,
    backlog_risk_score,
    risk_level
FROM daily_operations
WHERE risk_level = 'High'
ORDER BY backlog_risk_score DESC;
