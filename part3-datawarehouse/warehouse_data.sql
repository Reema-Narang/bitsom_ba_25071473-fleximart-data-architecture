USE fleximart_dw;

-- POPULATE dim_date (30 Days: Jan 2024)
INSERT INTO dim_date (date_key, full_date, day_of_week, day_of_month, month, month_name, quarter, year, is_weekend) VALUES
(20240101, '2024-01-01', 'Monday', 1, 1, 'January', 'Q1', 2024, 0), (20240102, '2024-01-02', 'Tuesday', 2, 1, 'January', 'Q1', 2024, 0),
(20240103, '2024-01-03', 'Wednesday', 3, 1, 'January', 'Q1', 2024, 0), (20240104, '2024-01-04', 'Thursday', 4, 1, 'January', 'Q1', 2024, 0),
(20240105, '2024-01-05', 'Friday', 5, 1, 'January', 'Q1', 2024, 0), (20240106, '2024-01-06', 'Saturday', 6, 1, 'January', 'Q1', 2024, 1),
(20240107, '2024-01-07', 'Sunday', 7, 1, 'January', 'Q1', 2024, 1), (20240108, '2024-01-08', 'Monday', 8, 1, 'January', 'Q1', 2024, 0),
(20240109, '2024-01-09', 'Tuesday', 9, 1, 'January', 'Q1', 2024, 0), (20240110, '2024-01-10', 'Wednesday', 10, 1, 'January', 'Q1', 2024, 0),
(20240111, '2024-01-11', 'Thursday', 11, 1, 'January', 'Q1', 2024, 0), (20240112, '2024-01-12', 'Friday', 12, 1, 'January', 'Q1', 2024, 0),
(20240113, '2024-01-13', 'Saturday', 13, 1, 'January', 'Q1', 2024, 1), (20240114, '2024-01-14', 'Sunday', 14, 1, 'January', 'Q1', 2024, 1),
(20240115, '2024-01-15', 'Monday', 15, 1, 'January', 'Q1', 2024, 0), (20240116, '2024-01-16', 'Tuesday', 16, 1, 'January', 'Q1', 2024, 0),
(20240117, '2024-01-17', 'Wednesday', 17, 1, 'January', 'Q1', 2024, 0), (20240118, '2024-01-18', 'Thursday', 18, 1, 'January', 'Q1', 2024, 0),
(20240119, '2024-01-19', 'Friday', 19, 1, 'January', 'Q1', 2024, 0), (20240120, '2024-01-20', 'Saturday', 20, 1, 'January', 'Q1', 2024, 1),
(20240121, '2024-01-21', 'Sunday', 21, 1, 'January', 'Q1', 2024, 1), (20240122, '2024-01-22', 'Monday', 22, 1, 'January', 'Q1', 2024, 0),
(20240123, '2024-01-23', 'Tuesday', 23, 1, 'January', 'Q1', 2024, 0), (20240124, '2024-01-24', 'Wednesday', 24, 1, 'January', 'Q1', 2024, 0),
(20240125, '2024-01-25', 'Thursday', 25, 1, 'January', 'Q1', 2024, 0), (20240126, '2024-01-26', 'Friday', 26, 1, 'January', 'Q1', 2024, 0),
(20240127, '2024-01-27', 'Saturday', 27, 1, 'January', 'Q1', 2024, 1), (20240128, '2024-01-28', 'Sunday', 28, 1, 'January', 'Q1', 2024, 1),
(20240129, '2024-01-29', 'Monday', 29, 1, 'January', 'Q1', 2024, 0), (20240130, '2024-01-30', 'Tuesday', 30, 1, 'January', 'Q1', 2024, 0);

-- POPULATE dim_product (15 Products)
INSERT INTO dim_product (product_id, product_name, category, subcategory, unit_price) VALUES
('P001', 'iPhone 15', 'Electronics', 'Mobile', 79900.00), ('P002', 'MacBook Air', 'Electronics', 'Laptop', 92000.00),
('P003', 'USB-C Cable', 'Electronics', 'Accessory', 999.00), ('P004', 'Bluetooth Mouse', 'Electronics', 'Accessory', 1500.00),
('P005', '27-inch Monitor', 'Electronics', 'Peripherals', 18000.00), ('P006', 'Cotton T-Shirt', 'Clothing', 'Men', 799.00),
('P007', 'Denim Jeans', 'Clothing', 'Men', 2499.00), ('P008', 'Running Shoes', 'Clothing', 'Footwear', 4500.00),
('P009', 'Winter Jacket', 'Clothing', 'Outerwear', 6500.00), ('P010', 'Ankle Socks', 'Clothing', 'Accessory', 199.00),
('P011', 'Ceramic Vase', 'Home', 'Decor', 1200.00), ('P012', 'Table Lamp', 'Home', 'Lighting', 3500.00),
('P013', 'Throw Pillow', 'Home', 'Textiles', 800.00), ('P014', 'Wall Clock', 'Home', 'Decor', 2200.00),
('P015', 'Scented Candle', 'Home', 'Decor', 450.00);

-- POPULATE dim_customer (12 Customers)
INSERT INTO dim_customer (customer_id, customer_name, city, state, customer_segment) VALUES
('C001', 'Arjun Mehta', 'Mumbai', 'Maharashtra', 'Retail'), ('C002', 'Sneha Rao', 'Mumbai', 'Maharashtra', 'Corporate'),
('C003', 'Amit Singh', 'Delhi', 'Delhi', 'Retail'), ('C004', 'Priya Sharma', 'Delhi', 'Delhi', 'Retail'),
('C005', 'Rohan Das', 'Bangalore', 'Karnataka', 'Corporate'), ('C006', 'Ananya Iyer', 'Bangalore', 'Karnataka', 'Retail'),
('C007', 'Vikram K.', 'Chennai', 'Tamil Nadu', 'Retail'), ('C008', 'Kavita B.', 'Chennai', 'Tamil Nadu', 'Corporate'),
('C009', 'Suresh P.', 'Mumbai', 'Maharashtra', 'Retail'), ('C010', 'Deepika L.', 'Delhi', 'Delhi', 'Corporate'),
('C011', 'Manish G.', 'Bangalore', 'Karnataka', 'Retail'), ('C012', 'Sunita V.', 'Chennai', 'Tamil Nadu', 'Retail');

-- POPULATE fact_sales (40 Transactions)
INSERT INTO fact_sales (date_key, product_key, customer_key, quantity_sold, unit_price, discount_amount, total_amount) VALUES
(20240102, 1, 2, 1, 79900.00, 0, 79900.00), (20240103, 3, 5, 5, 999.00, 500.00, 4495.00),
(20240106, 11, 1, 2, 1200.00, 100.00, 2300.00), (20240106, 6, 1, 3, 799.00, 0, 2397.00),
(20240107, 15, 4, 10, 450.00, 450.00, 4050.00), (20240107, 12, 4, 1, 3500.00, 0, 3500.00),
(20240109, 2, 5, 2, 92000.00, 5000.00, 179000.00), (20240110, 5, 8, 3, 18000.00, 1000.00, 53000.00),
(20240113, 8, 3, 1, 4500.00, 0, 4500.00), (20240113, 9, 3, 1, 6500.00, 500.00, 6000.00),
(20240114, 14, 6, 2, 2200.00, 200.00, 4200.00), (20240115, 4, 10, 2, 1500.00, 0, 3000.00),
(20240116, 7, 12, 1, 2499.00, 0, 2499.00), (20240117, 10, 11, 4, 199.00, 0, 796.00),
(20240120, 1, 9, 1, 79900.00, 2000.00, 77900.00), (20240120, 4, 9, 1, 1500.00, 0, 1500.00),
(20240121, 13, 7, 4, 800.00, 200.00, 3000.00), (20240121, 15, 7, 2, 450.00, 0, 900.00),
(20240122, 2, 2, 1, 92000.00, 0, 92000.00), (20240123, 5, 5, 1, 18000.00, 0, 18000.00),
(20240124, 3, 8, 10, 999.00, 999.00, 8991.00), (20240126, 6, 3, 2, 799.00, 0, 1598.00),
(20240127, 11, 4, 1, 1200.00, 0, 1200.00), (20240127, 12, 6, 1, 3500.00, 500.00, 3000.00),
(20240128, 8, 1, 1, 4500.00, 0, 4500.00), (20240128, 9, 11, 1, 6500.00, 0, 6500.00),
(20240128, 7, 12, 1, 2499.00, 0, 2499.00), (20240129, 1, 3, 1, 79900.00, 0, 79900.00),
(20240130, 4, 10, 1, 1500.00, 0, 1500.00), (20240102, 10, 2, 10, 199.00, 199.00, 1791.00),
(20240103, 14, 5, 1, 2200.00, 0, 2200.00), (20240106, 3, 1, 2, 999.00, 0, 1998.00),
(20240107, 5, 1, 1, 18000.00, 0, 18000.00), (20240113, 13, 8, 2, 800.00, 0, 1600.00),
(20240114, 15, 9, 5, 450.00, 250.00, 2000.00), (20240120, 6, 10, 1, 799.00, 0, 799.00),
(20240121, 2, 12, 1, 92000.00, 2000.00, 90000.00), (20240127, 8, 2, 1, 4500.00, 0, 4500.00),
(20240128, 1, 5, 1, 79900.00, 1000.00, 78900.00), (20240130, 12, 8, 1, 3500.00, 0, 3500.00);
