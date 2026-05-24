-- KPI query examples for portfolio analysis and dashboard validation.

-- 1. Customer and onboarding summary
SELECT
    COUNT(*) AS total_customers,
    COUNT(*) FILTER (WHERE customer_segment = 'Mass Affluent') AS mass_affluent_customers,
    COUNT(*) FILTER (WHERE risk_rating = 'High') AS high_risk_customers
FROM customers;

-- 2. Onboarding funnel by stage
SELECT
    onboarding_stage,
    COUNT(*) AS applications,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS percentage_of_total
FROM customer_onboarding
GROUP BY onboarding_stage
ORDER BY applications DESC;

-- 3. Average onboarding cycle time for completed applications
SELECT
    status,
    ROUND(AVG(completion_date - application_date), 2) AS avg_days_to_complete
FROM customer_onboarding
WHERE completion_date IS NOT NULL
GROUP BY status;

-- 4. Support ticket volume and SLA breach rate by category
SELECT
    ticket_category,
    COUNT(*) AS total_tickets,
    COUNT(*) FILTER (WHERE sla_breached) AS breached_tickets,
    ROUND(100.0 * COUNT(*) FILTER (WHERE sla_breached) / COUNT(*), 2) AS breach_rate_pct,
    ROUND(AVG(resolution_hours), 2) AS avg_resolution_hours
FROM support_tickets
GROUP BY ticket_category
ORDER BY total_tickets DESC;

-- 5. Support ticket channel mix
SELECT
    channel,
    COUNT(*) AS total_tickets,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS channel_share_pct
FROM support_tickets
GROUP BY channel
ORDER BY total_tickets DESC;

-- 6. Fraud operations summary
SELECT
    COUNT(*) AS total_fraud_cases,
    COUNT(*) FILTER (WHERE confirmed_fraud) AS confirmed_fraud_cases,
    ROUND(SUM(loss_amount), 2) AS total_loss_amount,
    ROUND(SUM(recovery_amount), 2) AS total_recovery_amount,
    ROUND(100.0 * SUM(recovery_amount) / NULLIF(SUM(loss_amount), 0), 2) AS recovery_rate_pct
FROM fraud_cases;

-- 7. Fraud cases by severity and status
SELECT
    severity,
    case_status,
    COUNT(*) AS cases
FROM fraud_cases
GROUP BY severity, case_status
ORDER BY severity, case_status;

-- 8. AI automation value by workflow area
SELECT
    workflow_area,
    COUNT(*) AS interactions,
    COUNT(*) FILTER (WHERE human_accepted) AS accepted_outputs,
    ROUND(100.0 * COUNT(*) FILTER (WHERE human_accepted) / COUNT(*), 2) AS acceptance_rate_pct,
    ROUND(SUM(estimated_minutes_saved), 2) AS total_minutes_saved
FROM ai_interactions
GROUP BY workflow_area
ORDER BY total_minutes_saved DESC;

-- 9. Employees using AI by department
SELECT
    d.department_name,
    COUNT(DISTINCT e.employee_id) AS employees_using_ai,
    COUNT(ai.ai_interaction_id) AS ai_interactions
FROM ai_interactions ai
JOIN employees e ON ai.employee_id = e.employee_id
JOIN departments d ON e.department_id = d.department_id
GROUP BY d.department_name
ORDER BY ai_interactions DESC;

-- 10. Daily executive KPI trend
SELECT
    DATE(created_at) AS report_date,
    COUNT(*) AS tickets_created,
    COUNT(*) FILTER (WHERE sla_breached) AS sla_breaches,
    COUNT(*) FILTER (WHERE ai_triaged) AS ai_triaged_tickets
FROM support_tickets
GROUP BY DATE(created_at)
ORDER BY report_date;
