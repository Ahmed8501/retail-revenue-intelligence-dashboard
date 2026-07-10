-- ============================================================
-- 03_clean_dimensions.sql
-- Purpose:
-- Clean products, stores, customers, marketing spend, and targets.
-- ============================================================

DROP TABLE IF EXISTS clean_products;

CREATE TABLE clean_products AS
SELECT
    product_id,
    product_name,
    COALESCE(NULLIF(TRIM(category), ''), 'Unknown') AS category,
    COALESCE(NULLIF(TRIM(subcategory), ''), 'Unknown') AS subcategory,
    COALESCE(NULLIF(TRIM(brand), ''), 'Unknown') AS brand,
    CAST(cost_price AS DOUBLE) AS cost_price
FROM raw_products;


DROP TABLE IF EXISTS clean_stores;

CREATE TABLE clean_stores AS
SELECT
    store_id,
    TRIM(store_name) AS store_name,
    UPPER(LEFT(TRIM(city), 1)) || LOWER(SUBSTRING(TRIM(city), 2)) AS city,    TRIM(region) AS region,
    TRIM(store_type) AS store_type
FROM raw_stores;


DROP TABLE IF EXISTS clean_customers;

CREATE TABLE clean_customers AS
SELECT
    customer_id,

    COALESCE(
        TRY_STRPTIME(signup_date, '%Y-%m-%d'),
        TRY_STRPTIME(signup_date, '%d/%m/%Y'),
        TRY_STRPTIME(signup_date, '%m-%d-%Y')
    )::DATE AS signup_date,

    TRIM(customer_segment) AS customer_segment,
    UPPER(LEFT(TRIM(city), 1)) || LOWER(SUBSTRING(TRIM(city), 2)) AS city,    TRIM(age_group) AS age_group
FROM raw_customers;


DROP TABLE IF EXISTS clean_marketing_spend;

CREATE TABLE clean_marketing_spend AS
SELECT
    COALESCE(
        TRY_STRPTIME(date, '%Y-%m-%d'),
        TRY_STRPTIME(date, '%d/%m/%Y'),
        TRY_STRPTIME(date, '%m-%d-%Y')
    )::DATE AS marketing_date,

    TRIM(channel) AS channel,
    TRIM(campaign_name) AS campaign_name,
    CAST(spend AS DOUBLE) AS spend,
    CAST(clicks AS INTEGER) AS clicks,
    CAST(impressions AS INTEGER) AS impressions,
    CAST(conversions AS INTEGER) AS conversions,
    CAST(attributed_revenue AS DOUBLE) AS attributed_revenue
FROM raw_marketing_spend;


DROP TABLE IF EXISTS clean_targets;

CREATE TABLE clean_targets AS
SELECT
    STRPTIME(month || '-01', '%Y-%m-%d')::DATE AS target_month,
    TRIM(region) AS region,
    CAST(revenue_target AS DOUBLE) AS revenue_target,
    CAST(profit_target AS DOUBLE) AS profit_target
FROM raw_targets;
