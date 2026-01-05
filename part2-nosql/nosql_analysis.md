Section A: Limitations of RDBMS
The current relational database (RDBMS) model relies on a fixed schema, which becomes a significant bottleneck as FlexiMart expands into diverse product categories.

Attribute Diversity & Sparse Tables: In MySQL, every row in the products table must follow the same column structure. If we add "RAM" for laptops and "Size" for shoes, the "Size" column remains NULL for laptops, and "RAM" remains NULL for shoes. As categories grow, the table becomes "sparse," wasting storage and complicating queries.

Schema Rigidity: Adding a new product type with unique attributes requires an ALTER TABLE command. In a production environment with millions of rows, this can cause significant downtime and requires complex migrations.

Nested Data Complexity: Storing customer reviews in an RDBMS typically requires a separate reviews table and complex JOIN operations. As the volume of reviews increases, these JOINs become computationally expensive, slowing down the product page load times.

Section B: NoSQL Benefits
MongoDB offers a document-oriented approach that aligns perfectly with FlexiMart's need for a highly diverse and rapidly changing product catalog.

Flexible Schema: MongoDB uses a BSON (Binary JSON) format, allowing each "document" (product) to have its own unique set of fields. A laptop document can contain technical specs, while a clothing document contains fabric details, all within the same products collection without requiring any schema changes.

Embedded Documents: Instead of separate tables for reviews, MongoDB allows FlexiMart to embed reviews directly within the product document. This "denormalization" means that a single query can fetch the product details and all its associated reviews simultaneously, eliminating the need for expensive JOINs and improving read performance.

Horizontal Scalability: MongoDB is designed for sharding, allowing data to be distributed across multiple servers. This ensures that as FlexiMart’s traffic grows, the database can scale out by adding more hardware rather than being limited to a single powerful server.

Section C: Trade-offs
While MongoDB provides flexibility, it introduces two primary disadvantages:

Data Redundancy and Inconsistency: Since MongoDB encourages denormalization (embedding data), information like a "Category Name" might be repeated in thousands of documents. If the category name changes, every single document must be updated, increasing the risk of data inconsistency compared to the "update once" nature of a normalized SQL database.

Increased Storage Overhead: In MongoDB, every document stores both the value and the field name (e.g., "product_name": "Laptop"). In an RDBMS, field names are stored once in the schema. This leads to significantly higher storage consumption for large datasets.