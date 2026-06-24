-- 1. Overall churn rate
SELECT
    COUNT(*)                                                AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)         AS churned,
    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    )                                                       AS churn_rate_pct
FROM customers;

-- 2. Revenue loss from churned customers
SELECT
    ROUND(SUM(monthlycharges), 2)                           AS total_monthly_revenue,
    ROUND(SUM(CASE WHEN churn = 'Yes'
              THEN monthlycharges ELSE 0 END), 2)           AS monthly_revenue_lost,
    ROUND(SUM(CASE WHEN churn = 'Yes'
              THEN totalcharges ELSE 0 END), 2)             AS total_revenue_lost
FROM customers;

-- 3. Churn by contract type
SELECT
    contract,
    COUNT(*)                                                AS total,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)         AS churned,
    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    )                                                       AS churn_rate_pct
FROM customers
GROUP BY contract
ORDER BY churn_rate_pct DESC;

-- 4. Churn by internet service
SELECT
    internetservice,
    COUNT(*)                                                AS total,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)         AS churned,
    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    )                                                       AS churn_rate_pct
FROM customers
GROUP BY internetservice
ORDER BY churn_rate_pct DESC;

-- 5. Average charges — churned vs retained
SELECT
    churn,
    ROUND(AVG(monthlycharges), 2)                           AS avg_monthly_charges,
    ROUND(AVG(totalcharges),   2)                           AS avg_total_charges,
    ROUND(AVG(tenure),         2)                           AS avg_tenure_months
FROM customers
GROUP BY churn;

-- 6. High-risk customers (not yet churned)
SELECT
    customerid,
    contract,
    tenure,
    monthlycharges,
    internetservice,
    paymentmethod
FROM customers
WHERE
    churn           = 'No'
    AND contract    = 'Month-to-month'
    AND tenure      < 12
    AND monthlycharges > 65
ORDER BY monthlycharges DESC;