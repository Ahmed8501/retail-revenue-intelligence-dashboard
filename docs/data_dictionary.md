# Data Dictionary

This document describes the synthetic retail dataset used in the Retail Revenue Intelligence Dashboard project.

The dataset represents a fictional retail and e-commerce company that sells products through physical stores and online channels. The data is intentionally designed to include realistic business issues such as missing values, inconsistent formats, duplicate records, returns, discounts, and target gaps.

## 1. orders.csv

The `orders.csv` file contains sales transaction records.

| Column            | Description                                        | Example       |
| ----------------- | -------------------------------------------------- | ------------- |
| `order_id`        | Unique identifier for each order                   | `ORD-100001`  |
| `order_date`      | Date when the order was placed                     | `2025-01-15`  |
| `customer_id`     | Identifier of the customer who placed the order    | `CUST-2045`   |
| `store_id`        | Identifier of the store or online channel location | `STORE-012`   |
| `product_id`      | Identifier of the purchased product                | `PROD-087`    |
| `quantity`        | Number of units purchased                          | `2`           |
| `unit_price`      | Selling price per unit before discount             | `49.99`       |
| `discount_amount` | Discount applied to the order line                 | `5.00`        |
| `payment_method`  | Payment method used by the customer                | `Credit Card` |
| `sales_channel`   | Channel where the sale happened                    | `Online`      |

## 2. returns.csv

The `returns.csv` file contains returned products and refund information.

| Column            | Description                          | Example        |
| ----------------- | ------------------------------------ | -------------- |
| `return_id`       | Unique identifier for each return    | `RET-50001`    |
| `order_id`        | Order linked to the returned product | `ORD-100001`   |
| `product_id`      | Product that was returned            | `PROD-087`     |
| `return_date`     | Date when the product was returned   | `2025-01-22`   |
| `return_reason`   | Reason for the return                | `Damaged item` |
| `refunded_amount` | Amount refunded to the customer      | `44.99`        |

## 3. products.csv

The `products.csv` file contains product master data.

| Column         | Description                                                | Example          |
| -------------- | ---------------------------------------------------------- | ---------------- |
| `product_id`   | Unique product identifier                                  | `PROD-087`       |
| `product_name` | Product name                                               | `Wireless Mouse` |
| `category`     | Main product category                                      | `Electronics`    |
| `subcategory`  | More detailed product category                             | `Accessories`    |
| `brand`        | Product brand                                              | `NovaTech`       |
| `cost_price`   | Cost paid by the company to acquire or produce the product | `25.00`          |

## 4. stores.csv

The `stores.csv` file contains store and region information.

| Column       | Description                     | Example                |
| ------------ | ------------------------------- | ---------------------- |
| `store_id`   | Unique store identifier         | `STORE-012`            |
| `store_name` | Store name                      | `Cairo Festival Store` |
| `city`       | City where the store is located | `Cairo`                |
| `region`     | Business region                 | `North`                |
| `store_type` | Type of store or sales location | `Physical Store`       |

## 5. customers.csv

The `customers.csv` file contains customer information.

| Column             | Description                   | Example              |
| ------------------ | ----------------------------- | -------------------- |
| `customer_id`      | Unique customer identifier    | `CUST-2045`          |
| `signup_date`      | Date when the customer joined | `2024-09-10`         |
| `customer_segment` | Customer segment              | `Returning Customer` |
| `city`             | Customer city                 | `Giza`               |
| `age_group`        | Customer age group            | `25-34`              |

## 6. marketing_spend.csv

The `marketing_spend.csv` file contains marketing campaign performance data.

| Column               | Description                        | Example                       |
| -------------------- | ---------------------------------- | ----------------------------- |
| `date`               | Campaign reporting date            | `2025-01-15`                  |
| `channel`            | Marketing channel                  | `Google Ads`                  |
| `campaign_name`      | Campaign name                      | `Winter Sale Search Campaign` |
| `spend`              | Marketing spend for the campaign   | `450.00`                      |
| `clicks`             | Number of ad clicks                | `1200`                        |
| `impressions`        | Number of ad impressions           | `25000`                       |
| `conversions`        | Number of conversions generated    | `85`                          |
| `attributed_revenue` | Revenue attributed to the campaign | `3200.00`                     |

## 7. targets.csv

The `targets.csv` file contains monthly revenue and profit targets by region.

| Column           | Description                 | Example     |
| ---------------- | --------------------------- | ----------- |
| `month`          | Target month                | `2025-01`   |
| `region`         | Business region             | `North`     |
| `revenue_target` | Monthly revenue target      | `250000.00` |
| `profit_target`  | Monthly gross profit target | `75000.00`  |

## 8. Designed Data Quality Issues

The dataset will intentionally include the following data quality issues to simulate a realistic freelance BI project:

| Issue                                 | Example                                           | Purpose                                       |
| ------------------------------------- | ------------------------------------------------- | --------------------------------------------- |
| Duplicate orders                      | Same `order_id` repeated                          | Practice deduplication                        |
| Missing customer IDs                  | Blank `customer_id` values                        | Handle guest checkout / missing customer data |
| Inconsistent date formats             | `2025-01-15`, `15/01/2025`                        | Practice date standardization                 |
| Inconsistent city names               | `Cairo`, `cairo`, `Cairo `                        | Practice text cleaning                        |
| Missing product categories            | Empty `category` values                           | Handle incomplete master data                 |
| Invalid discounts                     | Discount greater than expected                    | Detect suspicious business records            |
| Returns after original order date     | Normal return behavior                            | Model returns correctly                       |
| Marketing spend with zero conversions | Campaign spend without performance                | Analyze inefficient campaigns                 |
| Target gaps                           | Missing target for some region/month combinations | Handle incomplete planning data               |

## 9. Dataset Purpose

The dataset is designed to support the following analyses:

* Revenue analysis
* Profitability analysis
* Product performance analysis
* Store and region performance analysis
* Return rate analysis
* Marketing ROI analysis
* Target achievement analysis
* Business recommendation generation

