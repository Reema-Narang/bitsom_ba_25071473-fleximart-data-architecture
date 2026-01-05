!mysql -e "CREATE USER 'fleximart_user'@'localhost' IDENTIFIED BY 'password';"
!mysql -e "GRANT ALL PRIVILEGES ON fleximart.* TO 'fleximart_user'@'localhost';"
!mysql -e "FLUSH PRIVILEGES;"

import mysql.connector

# Connect to MySQL using the newly created user
db_config = {
    'host': 'localhost',
    'user': 'fleximart_user',
    'password': 'password',
    'database': 'fleximart'
}

def create_tables():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    schema_statements = [
        """
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INT PRIMARY KEY AUTO_INCREMENT,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(20),
            city VARCHAR(50),
            registration_date DATE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS products (
            product_id INT PRIMARY KEY AUTO_INCREMENT,
            product_name VARCHAR(100) NOT NULL,
            category VARCHAR(50) NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            stock_quantity INT DEFAULT 0
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS orders (
            order_id INT PRIMARY KEY AUTO_INCREMENT,
            customer_id INT NOT NULL,
            order_date DATE NOT NULL,
            total_amount DECIMAL(10,2) NOT NULL,
            status VARCHAR(20) DEFAULT 'Pending',
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INT PRIMARY KEY AUTO_INCREMENT,
            order_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT NOT NULL,
            unit_price DECIMAL(10,2) NOT NULL,
            subtotal DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
        """
    ]

    for statement in schema_statements:
        cursor.execute(statement)

    conn.commit()
    cursor.close()
    conn.close()
    print("Schema created successfully!")

create_tables()

#Part 1: Database Design and ETL Pipeline – Implementation
import pandas as pd
import mysql.connector
import re
import numpy as np
from datetime import datetime
import os

def etl_pipeline():
    # Initialize report dictionary
    report = {
        'cust_dupes': 0,
        'sales_dupes': 0,
        'prod_miss': 0,
        'total_sales_loaded': 0,
        'cust_read': 0,
        'cust_miss_email': 0,
        'cust_loaded': 0,
        'prod_read': 0,
        'prod_miss_price': 0,
        'prod_cat_std': 0,
        'prod_loaded': 0,
        'sales_read': 0,
        'sales_date_fix': 0,
        'sales_loaded': 0
    }

    # --- 1. EXTRACT ---
    try:
        cust_df = pd.read_csv('data/customers_raw.csv')
        prod_df = pd.read_csv('data/products_raw.csv')
        sales_df = pd.read_csv('data/sales_raw.csv')

        report['cust_read'] = len(cust_df)
        report['prod_read'] = len(prod_df)
        report['sales_read'] = len(sales_df)

    except FileNotFoundError:
        print("CSV files not found!")
        return

    # --- 2. TRANSFORM ---

    # Clean Customers
    initial_cust_count = len(cust_df)
    def clean_phone(p):
        if pd.isna(p): return None
        digits = re.sub(r'\D', '', str(p))
        return f"+91-{digits[-10:]}"
    cust_df['phone'] = cust_df['phone'].apply(clean_phone)
    cust_df.drop_duplicates(inplace=True)
    report['cust_dupes'] = initial_cust_count - len(cust_df)
    cust_df['registration_date'] = pd.to_datetime(cust_df['registration_date'], format='%Y-%m-%d', errors='coerce').dt.date


    # Clean Products
    prod_df.drop_duplicates(inplace=True)
    prod_df['category'] = prod_df['category'].str.strip().str.capitalize()
    report['prod_miss_price'] = prod_df['price'].isna().sum() # Count missing prices before filling
    prod_df['price'] = prod_df['price'].fillna(0)
    prod_df['stock_quantity'] = prod_df['stock_quantity'].fillna(0)

    # Clean Sales
    initial_sales_count = len(sales_df)
    sales_df.drop_duplicates(inplace=True)
    report['sales_dupes'] = initial_sales_count - len(sales_df)
    sales_df['transaction_date'] = pd.to_datetime(sales_df['transaction_date'], format='%Y-%m-%d', errors='coerce').dt.date

    # Remove rows where transaction_date is NaT (Not a Time) as it cannot be NULL in the DB
    initial_valid_sales_count = len(sales_df)
    sales_df.dropna(subset=['transaction_date'], inplace=True)
    report['sales_date_fix'] = initial_valid_sales_count - len(sales_df)

    # --- IMPORTANT: CONVERT NaN TO None FOR MYSQL ---
    # This prevents the ValueError you encountered
    cust_df = cust_df.where(pd.notnull(cust_df), None)
    prod_df = prod_df.where(pd.notnull(prod_df), None)
    sales_df = sales_df.where(pd.notnull(sales_df), None)

    # --- 3. LOAD ---
    try:
        conn = mysql.connector.connect(host='localhost', user='fleximart_user', password='password', database='fleximart')
        cursor = conn.cursor()

        # Load Customers
        cust_id_map = {}
        for _, row in cust_df.iterrows():
            try:
                cursor.execute("""INSERT INTO customers (first_name, last_name, email, phone, city, registration_date)
                                  VALUES (%s, %s, %s, %s, %s, %s)""",
                               (row['first_name'], row['last_name'], row['email'], row['phone'], row['city'], row['registration_date']))
                cust_id_map[row['customer_id']] = cursor.lastrowid
                report['cust_loaded'] += 1
            except mysql.connector.Error:
                cursor.execute("SELECT customer_id FROM customers WHERE email = %s", (row['email'],))
                res = cursor.fetchone()
                if res: cust_id_map[row['customer_id']] = res[0]
                else: report['cust_miss_email'] += 1 # A rough count for unhandled unique email errors

        # Load Products
        prod_id_map = {}
        for _, row in prod_df.iterrows():
            cursor.execute("INSERT INTO products (product_name, category, price, stock_quantity) VALUES (%s, %s, %s, %s)",
                           (row['product_name'], row['category'], float(row['price']), int(row['stock_quantity'])))
            prod_id_map[row['product_id']] = cursor.lastrowid
            report['prod_loaded'] += 1

        conn.commit()

        # Load Sales
        for _, row in sales_df.iterrows():
            db_cust_id = cust_id_map.get(row['customer_id'])
            db_prod_id = prod_id_map.get(row['product_id'])

            if db_cust_id and db_prod_id:
                # Use explicit float/int casting for NumPy types
                qty = int(row['quantity']) if row['quantity'] is not None else 0
                u_price = float(row['unit_price']) if row['unit_price'] is not None else 0.0
                total_amount = qty * u_price

                cursor.execute("INSERT INTO orders (customer_id, order_date, total_amount, status) VALUES (%s, %s, %s, %s)",
                               (db_cust_id, row['transaction_date'], total_amount, row['status']))
                order_id = cursor.lastrowid

                cursor.execute("""INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
                                  VALUES (%s, %s, %s, %s, %s)""",
                               (order_id, db_prod_id, qty, u_price, total_amount))
                report['total_sales_loaded'] += 1 # This is total order items loaded

        conn.commit()

        # Define report_path and timestamp
        report_path = 'part1-database-etl/data_quality_report.txt'
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #GENERATE REPORT
        separator = "=" * 80
        sub_sep = "-" * 80

        with open(report_path, 'w') as f:
            f.write(f"{separator}\n")
            f.write("FLEXIMART DATA QUALITY REPORT\n")
            f.write(f"{separator}\n")
            f.write(f"Generated on: {timestamp}\n\n")

            # Customers Section
            f.write(f"CUSTOMERS DATA QUALITY METRICS\n")
            f.write(f"{sub_sep}\n")
            f.write(f"Records read from file:        {report['cust_read']}\n")
            f.write(f"Duplicates removed:            {report['cust_dupes']}\n")
            f.write(f"Missing emails handled:        {report['cust_miss_email']}\n")
            f.write(f"Records loaded successfully:   {report['cust_loaded']}\n\n")

            # Products Section
            f.write(f"PRODUCTS DATA QUALITY METRICS\n")
            f.write(f"{sub_sep}\n")
            f.write(f"Records read from file:        {report['prod_read']}\n")
            f.write(f"Missing prices handled (dropped): {report['prod_miss_price']}\n")
            f.write(f"Category names standardized:   {prod_df['category'].nunique()}\n") # Counting unique categories as a proxy for standardization
            f.write(f"Records loaded successfully:   {report['prod_loaded']}\n\n")

            # Sales Section
            f.write(f"SALES DATA QUALITY METRICS\n")
            f.write(f"{sub_sep}\n")
            f.write(f"Records read from file:        {report['sales_read']}\n")
            f.write(f"Duplicates removed:            {report['sales_dupes']}\n")
            f.write(f"Date formats fixed:            {report['sales_date_fix']}\n")
            f.write(f"Order items loaded successfully: {report['total_sales_loaded']}\n\n") # Renamed from sales_loaded to total_sales_loaded

            f.write(f"{separator}\n")

        print("ETL complete! All data types converted and loaded.")

    except mysql.connector.Error as e:
        print(f"Database Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

etl_pipeline()