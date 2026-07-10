-- ============================================================
-- 01_create_clean_tables.sql
-- Purpose:
-- Create cleaned tables from raw CSV-loaded DuckDB tables.
-- ============================================================


-- -----------------------------
-- Clean products
-- -----------------------------

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


-- -----------------------------
-- Clean stores
-- -----------------------------

DROP TABLE IF EXISTS clean_stores;

CREATE TABLE clean_stores AS
SELECT
    store_id,
    TRIM(store_name) AS store_name,
    INITCAP(TRIM(city)) AS city,
    TRIM(region) AS region,
    TRIM(store_type) AS store_type
FROM raw_stores;


-- -----------------------------
-- Clean customers
-- -----------------------------

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
    INITCAP(TRIM(city)) AS city,
    TRIM(age_group) AS age_group
FROM raw_customers;


-- -----------------------------
-- Clean orders
-- -----------------------------
-- Notes:
-- 1. Deduplicate exact repeated order lines using ROW_NUMBER.
-- 2. Standardize mixed date formats.
-- 3. Replace missing customer IDs with 'GUEST'.
-- 4. Calculate gross sales and revenue.
-- 5. Flag suspicious discounts.
-- -----------------------------

DROP TABLE IF EXISTS clean_orders;

CREATE TABLE clean_orders AS
WITH deduplicated_orders AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY
                order_id,
                order_date,
                customer_id,
                store_id,
                product_id,
                quantity,
                unit_price,
                discount_amount,
                payment_method,
                sales_channel
            ORDER BY order_id
        ) AS row_num
    FROM raw_orders
),

standardized_orders AS (
    SELECT
        order_id,

        COALESCE(
            TRY_STRPTIME(order_date, '%Y-%m-%d'),
            TRY_STRPTIME(order_date, '%d/%m/%Y'),
            TRY_STRPTIME(order_date, '%m-%d-%Y')
        )::DATE AS order_date,

        COALESCE(NULLIF(TRIM(customer_id), ''), 'GUEST') AS customer_id,
        store_id,
        product_id,
        CAST(quantity AS INTEGER) AS quantity,
        CAST(unit_price AS DOUBLE) AS unit_price,
        CAST(discount_amount AS DOUBLE) AS discount_amount,
        TRIM(payment_method) AS payment_method,
        TRIM(sales_channel) AS sales_channel
    FROM deduplicated_orders
    WHERE row_num = 1
)

SELECT
    order_id,
    order_date,
    customer_id,
    store_id,
    product_id,
    quantity,
    unit_price,
    discount_amount,
    payment_method,
    sales_channel,

    quantity * unit_price AS gross_sales_before_discount,

    (quantity * unit_price) - discount_amount AS revenue,

    CASE
        WHEN discount_amount > quantity * unit_price THEN TRUE
        ELSE FALSE
    END AS is_suspicious_discount

FROM standardized_orders;


-- -----------------------------
-- Clean returns
-- -----------------------------

DROP TABLE IF EXISTS clean_returns;

CREATE TABLE clean_returns AS
SELECT
    return_id,
    order_id,
    product_id,

    COALESCE(
        TRY_STRPTIME(return_date, '%Y-%m-%d'),
        TRY_STRPTIME(return_date, '%d/%m/%Y'),
        TRY_STRPTIME(return_date, '%m-%d-%Y')
    )::DATE AS return_date,

    TRIM(return_reason) AS return_reason,
    CAST(refunded_amount AS DOUBLE) AS refunded_amount
FROM raw_returns;


-- -----------------------------
-- Clean marketing spend
-- -----------------------------

DROP TABLE IF EXISTS clean_marketing_spend;

CREATE TABLE clean_marketing_spend AS
SELECT
    COALESCE(
        TRY_STRPTIME(date, '%Y-%m-%d'),
        TRY_STRPTIME(date, '%d/%m/%Y'),
        TRY_STRPTIME(date, '%m-%d-%Y')
    )::DATE AS marketing_date,

    TRIM(channel) AS channel,
    TRIM (campaign_name) AS campaign_name,
    CAST(spend AS DOUBLE) AS spend,
    CAST(clicks AS INTEGER) AS clicks,
    CAST(impressions AS INTEGER) AS impressions,
    CAST(conversions AS INTEGER) AS conversions,
    CAST(attributed_revenue AS DOUBLE) AS attributed_revenue
FROM raw_marketing_spend;


-- -----------------------------
-- Clean targets
-- -----------------------------

DROP TABLE IF EXISTS clean_targets;

CREATE TABLE clean_targets AS
SELECT
    STRPTIME(month || '-01', '%Y-%m-%d')::DATE AS target_month,
    TRIM(region) AS region,
    CAST(revenue_target AS DOUBLE) AS revenue_target,
    CAST(profit_target AS DOUBLE) AS profit_target
FROM raw_targets;
