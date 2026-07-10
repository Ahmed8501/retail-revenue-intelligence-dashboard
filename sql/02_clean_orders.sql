-- ============================================================
-- 02_clean_orders.sql
-- Purpose:
-- Clean raw_orders and raw_returns.
-- ============================================================

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