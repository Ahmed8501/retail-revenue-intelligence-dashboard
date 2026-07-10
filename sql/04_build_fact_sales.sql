-- ============================================================
-- 04_build_fact_sales.sql
-- Purpose:
-- Build analytical fact and dimension tables from clean tables.
-- ============================================================


-- -----------------------------
-- Dimension: Product
-- -----------------------------

DROP TABLE IF EXISTS dim_product;

CREATE TABLE dim_product AS
SELECT
    product_id,
    product_name,
    category,
    subcategory,
    brand,
    cost_price
FROM clean_products;


-- -----------------------------
-- Dimension: Store
-- -----------------------------

DROP TABLE IF EXISTS dim_store;

CREATE TABLE dim_store AS
SELECT
    store_id,
    store_name,
    city,
    region,
    store_type
FROM clean_stores;


-- -----------------------------
-- Dimension: Customer
-- -----------------------------

DROP TABLE IF EXISTS dim_customer;

CREATE TABLE dim_customer AS
SELECT
    customer_id,
    signup_date,
    customer_segment,
    city,
    age_group
FROM clean_customers

UNION ALL

SELECT
    'GUEST' AS customer_id,
    NULL::DATE AS signup_date,
    'Guest Customer' AS customer_segment,
    'Unknown' AS city,
    'Unknown' AS age_group;


-- -----------------------------
-- Fact: Sales
-- -----------------------------

DROP TABLE IF EXISTS fact_sales;

CREATE TABLE fact_sales AS
SELECT
    o.order_id,
    o.order_date,
    DATE_TRUNC('month', o.order_date)::DATE AS order_month,

    o.customer_id,
    o.store_id,
    o.product_id,

    o.quantity,
    o.unit_price,
    o.discount_amount,
    o.gross_sales_before_discount,
    o.revenue,

    p.cost_price,
    o.quantity * p.cost_price AS product_cost,
    o.revenue - (o.quantity * p.cost_price) AS gross_profit,

    CASE
        WHEN o.revenue = 0 THEN NULL
        ELSE (o.revenue - (o.quantity * p.cost_price)) / o.revenue
    END AS gross_margin_pct,

    o.payment_method,
    o.sales_channel,
    o.is_suspicious_discount

FROM clean_orders o
LEFT JOIN clean_products p
    ON o.product_id = p.product_id;


-- -----------------------------
-- Fact: Returns
-- -----------------------------

DROP TABLE IF EXISTS fact_returns;

CREATE TABLE fact_returns AS
SELECT
    r.return_id,
    r.order_id,
    r.product_id,
    r.return_date,
    DATE_TRUNC('month', r.return_date)::DATE AS return_month,
    r.return_reason,
    r.refunded_amount,

    s.order_date,
    s.customer_id,
    s.store_id,
    s.sales_channel

FROM clean_returns r
LEFT JOIN fact_sales s
    ON r.order_id = s.order_id
    AND r.product_id = s.product_id;


-- -----------------------------
-- Fact: Marketing
-- -----------------------------

DROP TABLE IF EXISTS fact_marketing;

CREATE TABLE fact_marketing AS
SELECT
    marketing_date,
    DATE_TRUNC('month', marketing_date)::DATE AS marketing_month,
    channel,
    campaign_name,
    spend,
    clicks,
    impressions,
    conversions,
    attributed_revenue,

    CASE
        WHEN spend = 0 THEN NULL
        ELSE attributed_revenue / spend
    END AS roas,

    CASE
        WHEN conversions = 0 THEN NULL
        ELSE spend / conversions
    END AS cost_per_conversion,

    CASE
        WHEN clicks = 0 THEN NULL
        ELSE conversions::DOUBLE / clicks
    END AS conversion_rate_pct,

    CASE
        WHEN impressions = 0 THEN NULL
        ELSE clicks::DOUBLE / impressions
    END AS click_through_rate_pct

FROM clean_marketing_spend;


-- -----------------------------
-- Monthly Targets
-- -----------------------------

DROP TABLE IF EXISTS monthly_targets;

CREATE TABLE monthly_targets AS
SELECT
    target_month,
    region,
    revenue_target,
    profit_target
FROM clean_targets;
