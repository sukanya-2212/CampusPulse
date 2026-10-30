-- KPI-04: Fee Payment Analysis
-- Business question:
-- How are fee records distributed by type and payment status?

SELECT
    fee_type,
    payment_status,
    COUNT(*) AS total_records,
    ROUND(SUM(amount), 2) AS total_recorded_amount
FROM fees
GROUP BY
    fee_type,
    payment_status
ORDER BY
    fee_type,
    payment_status;