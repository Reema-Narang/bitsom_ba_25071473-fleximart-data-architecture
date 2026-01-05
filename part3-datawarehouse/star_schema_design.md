# FlexiMart Star Schema Design Documentation

## Section 1: Schema Overview

**FACT TABLE: fact_sales**
* **Grain:** One row per product per order line item.
* **Business Process:** Sales transactions recording individual item purchases.
* **Measures (Numeric Facts):**
    * `quantity_sold`: Total units sold for a specific line item.
    * `unit_price`: Price per unit at the time of sale.
    * `discount_amount`: Monetary value of the discount applied.
    * `total_amount`: Final revenue calculated as $(quantity \times unit\_price) - discount$.
* **Foreign Keys:**
    * `date_key` \u2192 dim_date (Standardized time reference)
    * `product_key` \u2192 dim_product (Product metadata)
    * `customer_key` \u2192 dim_customer (Customer demographics)

**DIMENSION TABLE: dim_date**
* **Purpose:** Date dimension for time-based analysis.
* **Type:** Conformed dimension.
* **Attributes:**
    * `date_key` (PK): Surrogate key (Integer: YYYYMMDD).
    * `full_date`: The specific calendar date.
    * `day_of_week`: Monday, Tuesday, etc.
    * `month`: Numeric month (1-12).
    * `month_name`: January, February, etc.
    * `quarter`: Q1, Q2, Q3, or Q4.
    * `year`: The calendar year (e.g., 2024).
    * `is_weekend`: Boolean flag (True/False).

**DIMENSION TABLE: dim_product**
* **Purpose:** Contains descriptive attributes for every product sold.
* **Attributes:**
    * `product_key` (PK): Surrogate key (Auto-incrementing integer).
    * `product_id`: Original Natural Key from the operational system.
    * `product_name`: Full name of the product.
    * `category`: Broad category (e.g., Electronics).
    * `sub_category`: Specific category (e.g., Audio).
    * `brand`: Manufacturer brand name.

**DIMENSION TABLE: dim_customer**
* **Purpose:** Stores demographic data to analyze buying patterns.
* **Attributes:**
    * `customer_key` (PK): Surrogate key.
    * `customer_id`: Original Natural Key.
    * `full_name`: Combined first and last name.
    * `city`: Primary city of the customer.
    * `region`: Geographic region (North, South, etc.).
    * `segment`: Customer type (e.g., Individual, Corporate).

---

## Section 2: Design Decisions

**Granularity Selection**
I chose the **transaction line-item level** granularity. This is the lowest atomic level available, which provides maximum flexibility. It allows FlexiMart to aggregate data upward to any level (by date, by category, or by city) without losing the ability to analyze specific product performance within a single order.

**Surrogate Keys vs. Natural Keys**
The design utilizes **surrogate keys** (integers) instead of natural keys (like Product IDs or Emails). Surrogate keys offer two main benefits: first, they protect the Data Warehouse from changes in the source system (e.g., if a Product ID is reused); second, integer-based joins are significantly faster and more storage-efficient than string-based joins in large analytical datasets.

**Support for Drill-down and Roll-up**
The hierarchies built into the dimensions support OLAP operations. For example, a user can **roll up** from specific dates to see quarterly revenue trends, or **drill down** from a geographic region into specific cities to identify underperforming local markets.

---

## Section 3: Sample Data Flow

**Source Transaction:**
* Order #101, Customer "John Doe", Product "Laptop", Qty: 2, Price: 50000

**Becomes in Data Warehouse:**

**fact_sales:**
| date_key | product_key | customer_key | quantity_sold | unit_price | total_amount |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 20240115 | 5 | 12 | 2 | 50000 | 100000 |

**dim_date:**
* `{date_key: 20240115, full_date: '2024-01-15', month: 1, quarter: 'Q1', month_name: 'January'}`

**dim_product:**
* `{product_key: 5, product_name: 'Laptop', category: 'Electronics', brand: 'GenericTech'}`

**dim_customer:**
* `{customer_key: 12, full_name: 'John Doe', city: 'Mumbai', region: 'West'}`
