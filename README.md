# FlexiMart Data Architecture Project

**Student Name:** Reema Narang 

**Student ID:** bitsom_ba_25071473 

**Email:** reema.narang4@gmail.com 

**Date:** January 2026 


## Project Overview
This project involves building a multi-layered data architecture for FlexiMart. I implemented a relational ETL pipeline for transactional data, a NoSQL MongoDB solution for a flexible product catalog, and a Star Schema Data Warehouse for advanced OLAP analytics and business intelligence.

## Repository Structure
├── part1-database-etl/ 

│   ├── etl_pipeline.py 

│   ├── schema_documentation.md 

│   ├── business_queries.sql 

│   └── data_quality_report.txt 

├── part2-nosql/ 

│   ├── nosql_analysis.md 

│   ├── mongodb_operations.js 

│   └── products_catalog.json 

├── part3-datawarehouse/ 

│   ├── star_schema_design.md 

│   ├── warehouse_schema.sql 

│   ├── warehouse_data.sql 

│   └── analytics_queries.sql 

└── README.md 


## Technologies Used
- Python 3.x, pandas, mysql-connector-python
- MySQL 8.0 / PostgreSQL 14
- MongoDB 6.0

## Setup Instructions

### Database Setup
```bash
# Create databases
mysql -u root -p -e "CREATE DATABASE fleximart;"
mysql -u root -p -e "CREATE DATABASE fleximart_dw;"

# Run Part 1 - ETL Pipeline
python part1-database-etl/etl_pipeline.py

# Run Part 3 - Data Warehouse Implementation
mysql -u fleximart_user -ppassword fleximart_dw < part3-datawarehouse/warehouse_schema.sql
mysql -u fleximart_user -ppassword fleximart_dw < part3-datawarehouse/warehouse_data.sql
mysql -u fleximart_user -ppassword fleximart_dw < part3-datawarehouse/analytics_queries.sql
```
## MongoDB Setup

mongosh < part2-nosql/mongodb_operations.js 

## Key Learnings
Learned how to manage schema evolution by using MongoDB for diverse product attributes.

Mastered the creation of Star Schemas to optimize query performance for massive datasets.

Implemented complex SQL window functions to calculate business metrics like revenue contribution percentages.

## Challenges Faced
Challenge: Handling foreign key constraints during the Data Warehouse load.

Solution: Ensured dimension tables were populated with conformed data before the fact table.

Challenge: Calculating percentages in SQL without subqueries.

Solution: Utilized Window Functions (OVER clause) to get total revenue across all rows for the denominator.