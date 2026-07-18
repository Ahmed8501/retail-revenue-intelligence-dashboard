-- ============================================================
-- 05_build_kpi_views.sql
-- Purpose:
-- Build dashboard-ready KPI views for Power BI.
-- ============================================================


-- -----------------------------
-- Executive Overview
-- -----------------------------

DROP VIEW IF EXISTS vw_executive_overview;

CREATE VIEW vw_executive_overview AS
WITH sales AS (
    SELECT
        fs.order_month,
        ds.region,
        fs.sales_channel,

        SUM(fs.revenue) AS revenue,
        SUM(fs.gross_profit) AS gross_profit,
        SUM(fs.quantity) AS units_sold,
        COUNT(DISTINCT fs.order_id) AS total_orders,
        SUM(fs.discount_amount) AS discount_amount,
        SUM(fs.gross_sales_before_discount) AS gross_sales_before_discount

    FROM fact_sales fs
    LEFT JOIN dim_store ds
        ON fs.store_id = ds.store_id
    GROUP BY
        fs.order_month,
        ds.region,
        fs.sales_channel
),

returns AS (
    SELECT
        DATE_TRUNC('month', fr.return_date)::DATE AS return_month,
        ds.region,
        fr.sales_channel,

        COUNT(DISTINCT fr.order_id) AS returned_orders,
        SUM(fr.refunded_amount) AS return_amount

    FROM fact_returns fr
    LEFT JOIN dim_store ds
        ON fr.store_id = ds.store_id
    GROUP BY
        DATE_TRUNC('month', fr.return_date)::DATE,
        ds.region,
        fr.sales_channel
)

SELECT
    s.order_month,
    s.region,
    s.sales_channel,

    s.revenue,
    s.gross_profit,

    CASE
        WHEN s.revenue = 0 THEN NULL
        ELSE s.gross_profit / s.revenue
    END AS gross_margin_pct,

    s.units_sold,
    s.total_orders,

    CASE
        WHEN s.total_orders = 0 THEN NULL
        ELSE s.revenue / s.total_orders
    END AS average_order_value,

    COALESCE(r.returned_orders, 0) AS returned_orders,
    COALESCE(r.return_amount, 0) AS return_amount,

    CASE
        WHEN s.total_orders = 0 THEN NULL
        ELSE COALESCE(r.returned_orders, 0)::DOUBLE / s.total_orders
    END AS return_rate_pct,

    s.discount_amount,
    s.gross_sales_before_discount,

    CASE
        WHEN s.gross_sales_before_discount = 0 THEN NULL
        ELSE s.discount_amount / s.gross_sales_before_discount
    END AS discount_rate_pct,

    mt.revenue_target,
    mt.profit_target,

    CASE
        WHEN mt.revenue_target IS NULL OR mt.revenue_target = 0 THEN NULL
        ELSE s.revenue / mt.revenue_target
    END AS revenue_target_achievement_pct,

    CASE
        WHEN mt.profit_target IS NULL OR mt.profit_target = 0 THEN NULL
        ELSE s.gross_profit / mt.profit_target
    END AS profit_target_achievement_pct

FROM sales s
LEFT JOIN returns r
    ON s.order_month = r.return_month
    AND s.region = r.region
    AND s.sales_channel = r.sales_channel
LEFT JOIN monthly_targets mt
    ON s.order_month = mt.target_month
    AND s.region = mt.region;


-- -----------------------------
-- Product Performance
-- -----------------------------

DROP VIEW IF EXISTS vw_product_performance;

CREATE VIEW vw_product_performance AS
WITH sales AS (
    SELECT
        dp.product_id,
        dp.product_name,
        dp.category,
        dp.subcategory,
        dp.brand,

        SUM(fs.revenue) AS revenue,
        SUM(fs.gross_profit) AS gross_profit,
        SUM(fs.quantity) AS units_sold,
        COUNT(DISTINCT fs.order_id) AS total_orders,
        SUM(fs.discount_amount) AS discount_amount,
        SUM(fs.gross_sales_before_discount) AS gross_sales_before_discount

    FROM fact_sales fs
    LEFT JOIN dim_product dp
        ON fs.product_id = dp.product_id
    GROUP BY
        dp.product_id,
        dp.product_name,
        dp.category,
        dp.subcategory,
        dp.brand
),

returns AS (
    SELECT
        product_id,
        COUNT(DISTINCT order_id) AS returned_orders,
        SUM(refunded_amount) AS return_amount
    FROM fact_returns
    GROUP BY product_id
)

SELECT
    s.product_id,
    s.product_name,
    s.category,
    s.subcategory,
    s.brand,

    s.revenue,
    s.gross_profit,

    CASE
        WHEN s.revenue = 0 THEN NULL
        ELSE s.gross_profit / s.revenue
    END AS gross_margin_pct,

    s.units_sold,
    s.total_orders,

    COALESCE(r.returned_orders, 0) AS returned_orders,
    COALESCE(r.return_amount, 0) AS return_amount,

    CASE
        WHEN s.total_orders = 0 THEN NULL
        ELSE COALESCE(r.returned_orders, 0)::DOUBLE / s.total_orders
    END AS return_rate_pct,

    s.discount_amount,
    s.gross_sales_before_discount,

    CASE
        WHEN s.gross_sales_before_discount = 0 THEN NULL
        ELSE s.discount_amount / s.gross_sales_before_discount
    END AS discount_rate_pct

FROM sales s
LEFT JOIN returns r
    ON s.product_id = r.product_id;


-- -----------------------------
-- Store and Region Performance
-- -----------------------------

DROP VIEW IF EXISTS vw_store_region_performance;

CREATE VIEW vw_store_region_performance AS
WITH sales AS (
    SELECT
        ds.store_id,
        ds.store_name,
        ds.city,
        ds.region,
        ds.store_type,
        fs.order_month,

        SUM(fs.revenue) AS revenue,
        SUM(fs.gross_profit) AS gross_profit,
        SUM(fs.quantity) AS units_sold,
        COUNT(DISTINCT fs.order_id) AS total_orders

    FROM fact_sales fs
    LEFT JOIN dim_store ds
        ON fs.store_id = ds.store_id
    GROUP BY
        ds.store_id,
        ds.store_name,
        ds.city,
        ds.region,
        ds.store_type,
        fs.order_month
),

returns AS (
    SELECT
        fr.store_id,
        DATE_TRUNC('month', fr.return_date)::DATE AS return_month,

        COUNT(DISTINCT fr.order_id) AS returned_orders,
        SUM(fr.refunded_amount) AS return_amount

    FROM fact_returns fr
    GROUP BY
        fr.store_id,
        DATE_TRUNC('month', fr.return_date)::DATE
)

SELECT
    s.store_id,
    s.store_name,
    s.city,
    s.region,
    s.store_type,
    s.order_month,

    s.revenue,
    s.gross_profit,

    CASE
        WHEN s.revenue = 0 THEN NULL
        ELSE s.gross_profit / s.revenue
    END AS gross_margin_pct,

    s.units_sold,
    s.total_orders,

    COALESCE(r.returned_orders, 0) AS returned_orders,
    COALESCE(r.return_amount, 0) AS return_amount,

    CASE
        WHEN s.total_orders = 0 THEN NULL
        ELSE COALESCE(r.returned_orders, 0)::DOUBLE / s.total_orders
    END AS return_rate_pct,

    mt.revenue_target,
    mt.profit_target,

    CASE
        WHEN mt.revenue_target IS NULL OR mt.revenue_target = 0 THEN NULL
        ELSE s.revenue / mt.revenue_target
    END AS revenue_target_achievement_pct,

    CASE
        WHEN mt.profit_target IS NULL OR mt.profit_target = 0 THEN NULL
        ELSE s.gross_profit / mt.profit_target
    END AS profit_target_achievement_pct

FROM sales s
LEFT JOIN returns r
    ON s.store_id = r.store_id
    AND s.order_month = r.return_month
LEFT JOIN monthly_targets mt
    ON s.order_month = mt.target_month
    AND s.region = mt.region;


-- -----------------------------
-- Marketing ROI
-- -----------------------------

DROP VIEW IF EXISTS vw_marketing_roi;

CREATE VIEW vw_marketing_roi AS
SELECT
    marketing_month,
    channel,
    campaign_name,

    SUM(spend) AS spend,
    SUM(attributed_revenue) AS attributed_revenue,
    SUM(clicks) AS clicks,
    SUM(impressions) AS impressions,
    SUM(conversions) AS conversions,

    CASE
        WHEN SUM(spend) = 0 THEN NULL
        ELSE SUM(attributed_revenue) / SUM(spend)
    END AS roas,

    CASE
        WHEN SUM(conversions) = 0 THEN NULL
        ELSE SUM(spend) / SUM(conversions)
    END AS cost_per_conversion,

    CASE
        WHEN SUM(clicks) = 0 THEN NULL
        ELSE SUM(conversions)::DOUBLE / SUM(clicks)
    END AS conversion_rate_pct,

    CASE
        WHEN SUM(impressions) = 0 THEN NULL
        ELSE SUM(clicks)::DOUBLE / SUM(impressions)
    END AS click_through_rate_pct

FROM fact_marketing
GROUP BY
    marketing_month,
    channel,
    campaign_name;
