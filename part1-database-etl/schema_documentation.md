# FlexiMart Database Schema Documentation

## 1. Entity-Relationship Description

**ENTITY: customers**
* **Purpose:** Stores customer profile and contact details.
* **Attributes:**
    * `customer_id`: Unique identifier (Primary Key).
    * `first_name`: Customer's first name.
    * `last_name`: Customer's last name.
    * `email`: Unique email address.
    * `phone`: Standardized phone number (+91-XXXXXXXXXX).
    * `city`: City of residence.
    * `registration_date`: Date the account was created.
* **Relationships:**
    * **1:M with `orders`**: One customer can place multiple orders.

**ENTITY: products**
* **Purpose:** Stores the product catalog and inventory levels.
* **Attributes:**
    * `product_id`: Unique identifier (Primary Key).
    * `product_name`: Name of the item.
    * `category`: Standardized category name (e.g., Electronics).
    * `price`: Unit price of the product.
    * `stock_quantity`: Current stock level.
* **Relationships:**
    * **1:M with `order_items`**: One product can appear in many order line items.

**ENTITY: orders**
* **Purpose:** Transaction headers for each purchase.
* **Attributes:**
    * `order_id`: Unique identifier (Primary Key).
    * `customer_id`: Foreign Key linking to customers.
    * `order_date`: Date of transaction (YYYY-MM-DD).
    * `total_amount`: Total value of the order.
    * `status`: Current order status (e.g., Completed, Pending).
* **Relationships:**
    * **1:M with `order_items`**: One order contains multiple line items.

**ENTITY: order_items**
* **Purpose:** Junction table storing details for each specific item in an order.
* **Attributes:**
    * `order_item_id`: Unique identifier (Primary Key).
    * `order_id`: Foreign Key linking to orders.
    * `product_id`: Foreign Key linking to products.
    * `quantity`: Number of units purchased.
    * `unit_price`: Price at time of purchase.
    * `subtotal`: quantity * unit_price.

---

## 2. Normalization Explanation (3NF)

The FlexiMart database design is structured in **Third Normal Form (3NF)** to ensure high data integrity and minimal redundancy.

**Functional Dependencies:**
Every non-key attribute is functionally dependent solely on the primary key. In `customers`, attributes like `email` and `city` depend only on `customer_id`. In `orders`, the `order_date` depends on the `order_id`.

**Why it is in 3NF:**
The design satisfies **1NF** by using atomic values (no lists of products in one cell) and **2NF** by ensuring no partial dependencies (all attributes in `order_items` depend on the composite relationship of order and product). It reaches **3NF** because there are no **transitive dependencies**. For example, we do not store the customer’s city in the `orders` table. If we did, city would depend on `customer_id`, which depends on `order_id`. By moving city to the `customers` table, we ensure all attributes depend *only* on the primary key.

**Anomaly Avoidance:**
- **Insert Anomaly:** We can add a new product to the catalog without waiting for it to be sold.
- **Update Anomaly:** If a customer changes their phone number, we update it in one place (customers table), and it reflects across all their historical orders.
- **Delete Anomaly:** Deleting a specific order line item doesn't accidentally delete the customer's account or the product's existence from the system.

---

## 3. Sample Data Representation

### Table: customers
| customer_id | first_name | email | city |
| :--- | :--- | :--- | :--- |
| 1 | Ravi | ravi@test.com | Mumbai |
| 2 | Priya | priya@test.com | Delhi |

### Table: products
| product_id | product_name | category | price |
| :--- | :--- | :--- | :--- |
| 101 | Laptop | Electronics | 55000.00 |
| 102 | Mouse | Electronics | 800.00 |
