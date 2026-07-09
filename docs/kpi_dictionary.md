# KPI Dictionary

This document defines the key performance indicators used in the Retail Revenue Intelligence Dashboard project.

The purpose of this KPI dictionary is to make business metrics consistent, transparent, and easy to understand across the dashboard.

## 1. Revenue

### Definition

Revenue represents the total sales amount after applying discounts.

### Formula

```sql
Revenue = (quantity * unit_price) - discount_amount
```

### Business Meaning

Revenue shows how much money the company generated from sales before subtracting product costs, refunds, or marketing spend.

### Used In

* Executive Overview
* Product Performance
* Store and Region Performance
* Target Achievement Analysis

---

## 2. Gross Profit

### Definition

Gross profit represents revenue after subtracting the cost of sold products.

### Formula

```sql
Gross Profit = Revenue - Product Cost
```

Where:

```sql
Product Cost = quantity * cost_price
```

### Business Meaning

Gross profit shows how much money remains after covering the cost of the products sold.

### Used In

* Executive Overview
* Product Performance
* Store and Region Performance

---

## 3. Gross Margin %

### Definition

Gross margin percentage shows the percentage of revenue that remains as gross profit.

### Formula

```sql
Gross Margin % = Gross Profit / Revenue
```

### Business Meaning

Gross margin percentage helps evaluate profitability. A product or region may generate high revenue but still have weak profitability if costs, discounts, or returns are high.

### Used In

* Executive Overview
* Product Performance
* Store and Region Performance

---

## 4. Total Orders

### Definition

Total orders represent the number of unique customer orders.

### Formula

```sql
Total Orders = COUNT(DISTINCT order_id)
```

### Business Meaning

Total orders show the volume of customer purchases.

### Used In

* Executive Overview
* Sales Channel Analysis
* Store and Region Performance

---

## 5. Units Sold

### Definition

Units sold represent the total quantity of products sold.

### Formula

```sql
Units Sold = SUM(quantity)
```

### Business Meaning

Units sold help measure product demand and sales volume.

### Used In

* Product Performance
* Store and Region Performance
* Executive Overview

---

## 6. Average Order Value

### Definition

Average order value shows the average revenue generated per order.

### Formula

```sql
Average Order Value = Revenue / Total Orders
```

### Business Meaning

Average order value helps understand customer spending behavior. A higher value may indicate stronger basket size or better upselling.

### Used In

* Executive Overview
* Sales Channel Analysis
* Store and Region Performance

---

## 7. Return Amount

### Definition

Return amount represents the total refunded amount for returned products.

### Formula

```sql
Return Amount = SUM(refunded_amount)
```

### Business Meaning

Return amount shows how much revenue was lost due to product returns.

### Used In

* Executive Overview
* Product Performance
* Store and Region Performance

---

## 8. Returned Orders

### Definition

Returned orders represent the number of unique orders that had at least one returned product.

### Formula

```sql
Returned Orders = COUNT(DISTINCT order_id)
```

From the returns data.

### Business Meaning

Returned orders help identify how often customers return purchased products.

### Used In

* Executive Overview
* Product Performance
* Store and Region Performance

---

## 9. Return Rate %

### Definition

Return rate percentage shows the share of orders that resulted in a return.

### Formula

```sql
Return Rate % = Returned Orders / Total Orders
```

### Business Meaning

Return rate helps identify product quality issues, customer dissatisfaction, fulfillment problems, or misleading product expectations.

### Used In

* Executive Overview
* Product Performance
* Store and Region Performance

---

## 10. Net Revenue

### Definition

Net revenue represents revenue after subtracting refunded amounts.

### Formula

```sql
Net Revenue = Revenue - Return Amount
```

### Business Meaning

Net revenue gives a more realistic view of retained sales after customer returns.

### Used In

* Executive Overview
* Product Performance
* Store and Region Performance

---

## 11. Revenue Target Achievement %

### Definition

Revenue target achievement percentage compares actual revenue to the revenue target.

### Formula

```sql
Revenue Target Achievement % = Revenue / Revenue Target
```

### Business Meaning

This KPI shows whether the business, region, or store is meeting planned revenue goals.

### Used In

* Executive Overview
* Store and Region Performance

---

## 12. Profit Target Achievement %

### Definition

Profit target achievement percentage compares actual gross profit to the profit target.

### Formula

```sql
Profit Target Achievement % = Gross Profit / Profit Target
```

### Business Meaning

This KPI shows whether the business is meeting profitability goals, not only sales goals.

### Used In

* Executive Overview
* Store and Region Performance

---

## 13. Discount Amount

### Definition

Discount amount represents the total discount given to customers.

### Formula

```sql
Discount Amount = SUM(discount_amount)
```

### Business Meaning

Discount amount helps evaluate how promotions affect revenue and profitability.

### Used In

* Product Performance
* Executive Overview

---

## 14. Discount Rate %

### Definition

Discount rate percentage shows the discount amount as a share of gross sales before discount.

### Formula

```sql
Discount Rate % = Discount Amount / Gross Sales Before Discount
```

Where:

```sql
Gross Sales Before Discount = quantity * unit_price
```

### Business Meaning

This KPI helps identify products or categories where heavy discounting may be reducing profitability.

### Used In

* Product Performance
* Sales Channel Analysis

---

## 15. Marketing Spend

### Definition

Marketing spend represents the total amount spent on marketing campaigns.

### Formula

```sql
Marketing Spend = SUM(spend)
```

### Business Meaning

Marketing spend shows how much the company invested in customer acquisition and campaign activity.

### Used In

* Marketing ROI

---

## 16. Attributed Revenue

### Definition

Attributed revenue represents revenue linked to marketing campaigns.

### Formula

```sql
Attributed Revenue = SUM(attributed_revenue)
```

### Business Meaning

Attributed revenue helps evaluate how much sales activity can be connected to marketing efforts.

### Used In

* Marketing ROI

---

## 17. ROAS

### Definition

Return on ad spend measures how much attributed revenue is generated for each unit of marketing spend.

### Formula

```sql
ROAS = Attributed Revenue / Marketing Spend
```

### Business Meaning

ROAS helps compare marketing channel efficiency. A channel with high revenue is not always the best channel if its spend is also very high.

### Used In

* Marketing ROI

---

## 18. Cost per Conversion

### Definition

Cost per conversion shows how much marketing spend is required to generate one conversion.

### Formula

```sql
Cost per Conversion = Marketing Spend / Conversions
```

### Business Meaning

This KPI helps identify expensive or inefficient campaigns.

### Used In

* Marketing ROI

---

## 19. Conversion Rate %

### Definition

Conversion rate percentage shows the share of clicks that resulted in conversions.

### Formula

```sql
Conversion Rate % = Conversions / Clicks
```

### Business Meaning

Conversion rate helps measure the effectiveness of campaigns after users click on ads or marketing links.

### Used In

* Marketing ROI

---

## 20. Click-Through Rate %

### Definition

Click-through rate shows the share of impressions that resulted in clicks.

### Formula

```sql
Click-Through Rate % = Clicks / Impressions
```

### Business Meaning

Click-through rate helps measure whether campaigns are attracting user attention.

### Used In

* Marketing ROI

---

## Notes on KPI Handling

* Division-based KPIs should return `NULL` or blank when the denominator is zero.
* Revenue and profit KPIs should be rounded to two decimal places.
* Percentage KPIs should be formatted as percentages in the dashboard.
* Monetary KPIs should use a consistent currency format.
* Target achievement KPIs should be interpreted carefully when target data is missing.

