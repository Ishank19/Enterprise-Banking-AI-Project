-- Join customers with onboarding data

SELECT
    c.customer_id,
    c.customer_name,
    c.country,
    c.customer_segment,
    o.application_date,
    o.kyc_status,
    o.document_status,
    o.application_status,
    o.onboarding_channel,
    o.completion_date,
    o.onboarding_duration_days
FROM customers c
JOIN customer_onboarding o
    ON c.customer_id = o.customer_id;