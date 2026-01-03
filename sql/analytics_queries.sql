-- ============================================================
-- BUSINESS ANALYTICS QUERIES
-- E-commerce Data Analysis
-- ============================================================

-- ------------------------------------------------------------
-- 1. REVENUE ANALYTICS
-- ------------------------------------------------------------

-- Total Revenue
SELECT 
    SUM(total_amount) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders,
    AVG(total_amount) AS average_order_value
FROM orders
WHERE order_status = 'Completed';

-- Revenue by Date
SELECT 
    order_date,
    COUNT(order_id) AS orders_count,
    SUM(total_amount) AS daily_revenue,
    AVG(total_amount) AS avg_order_value
FROM orders
WHERE order_status = 'Completed'
GROUP BY order_date
ORDER BY order_date DESC;

-- Revenue Trends (Last 7 Days)
SELECT 
    order_date,
    SUM(total_amount) AS revenue,
    COUNT(order_id) AS order_count
FROM orders
WHERE order_status = 'Completed'
    AND order_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
GROUP BY order_date
ORDER BY order_date;

-- ------------------------------------------------------------
-- 2. CUSTOMER ANALYTICS
-- ------------------------------------------------------------

-- Top 10 Customers by Revenue
SELECT 
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.email,
    c.city,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_spent,
    AVG(o.total_amount) AS avg_order_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_status = 'Completed'
GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.city
ORDER BY total_spent DESC
LIMIT 10;

-- Customer Lifetime Value (CLV)
SELECT 
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    COUNT(o.order_id) AS purchase_frequency,
    SUM(o.total_amount) AS lifetime_value,
    AVG(o.total_amount) AS avg_transaction_value,
    MAX(o.order_date) AS last_purchase_date,
    DATEDIFF(CURDATE(), MAX(o.order_date)) AS days_since_purchase
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
    AND o.order_status = 'Completed'
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING lifetime_value > 0
ORDER BY lifetime_value DESC;

-- Customer Distribution by City
SELECT 
    c.city,
    c.state,
    COUNT(DISTINCT c.customer_id) AS customer_count,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_revenue
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
    AND o.order_status = 'Completed'
GROUP BY c.city, c.state
ORDER BY total_revenue DESC;

-- ------------------------------------------------------------
-- 3. PRODUCT ANALYTICS
-- ------------------------------------------------------------

-- Top 10 Best-Selling Products
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    p.price,
    COUNT(oi.order_item_id) AS times_ordered,
    SUM(oi.quantity) AS total_quantity_sold,
    SUM(oi.quantity * oi.price_per_unit) AS total_revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'Completed'
GROUP BY p.product_id, p.product_name, p.category, p.price
ORDER BY total_revenue DESC
LIMIT 10;

-- Product Performance by Category
SELECT 
    p.category,
    COUNT(DISTINCT p.product_id) AS products_count,
    SUM(oi.quantity) AS total_units_sold,
    SUM(oi.quantity * oi.price_per_unit) AS category_revenue,
    AVG(oi.price_per_unit) AS avg_product_price
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'Completed'
GROUP BY p.category
ORDER BY category_revenue DESC;

-- Low Stock Products (Inventory Alert)
SELECT 
    product_id,
    product_name,
    category,
    stock_quantity,
    price
FROM products
WHERE stock_quantity < 50
ORDER BY stock_quantity ASC;

-- ------------------------------------------------------------
-- 4. ORDER ANALYTICS
-- ------------------------------------------------------------

-- Orders Status Summary
SELECT 
    order_status,
    COUNT(order_id) AS order_count,
    SUM(total_amount) AS total_value,
    AVG(total_amount) AS avg_order_value
FROM orders
GROUP BY order_status
ORDER BY order_count DESC;

-- Average Items per Order
SELECT 
    AVG(items_per_order) AS avg_items_per_order,
    MAX(items_per_order) AS max_items_in_order,
    MIN(items_per_order) AS min_items_in_order
FROM (
    SELECT 
        order_id,
        COUNT(order_item_id) AS items_per_order
    FROM order_items
    GROUP BY order_id
) AS order_summary;

-- Orders by Day of Week
SELECT 
    DAYNAME(order_date) AS day_of_week,
    COUNT(order_id) AS order_count,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_order_value
FROM orders
WHERE order_status = 'Completed'
GROUP BY DAYNAME(order_date), DAYOFWEEK(order_date)
ORDER BY DAYOFWEEK(order_date);

-- ------------------------------------------------------------
-- 5. ADVANCED INSIGHTS
-- ------------------------------------------------------------

-- Customer Segmentation (RFM-like)
SELECT 
    customer_id,
    customer_name,
    CASE 
        WHEN total_spent >= 50000 THEN 'High Value'
        WHEN total_spent >= 20000 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS customer_segment,
    total_orders,
    total_spent,
    days_since_purchase
FROM (
    SELECT 
        c.customer_id,
        CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
        COUNT(o.order_id) AS total_orders,
        SUM(o.total_amount) AS total_spent,
        DATEDIFF(CURDATE(), MAX(o.order_date)) AS days_since_purchase
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.order_status = 'Completed'
    GROUP BY c.customer_id, c.first_name, c.last_name
) AS customer_summary
ORDER BY total_spent DESC;

-- Product Cross-Sell Analysis
-- (Products frequently bought together)
SELECT 
    oi1.product_id AS product_1,
    p1.product_name AS product_1_name,
    oi2.product_id AS product_2,
    p2.product_name AS product_2_name,
    COUNT(*) AS times_bought_together
FROM order_items oi1
JOIN order_items oi2 ON oi1.order_id = oi2.order_id
    AND oi1.product_id < oi2.product_id
JOIN products p1 ON oi1.product_id = p1.product_id
JOIN products p2 ON oi2.product_id = p2.product_id
GROUP BY oi1.product_id, p1.product_name, oi2.product_id, p2.product_name
HAVING times_bought_together >= 2
ORDER BY times_bought_together DESC
LIMIT 10;

-- Revenue Contribution by Customer
SELECT 
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    SUM(o.total_amount) AS customer_revenue,
    ROUND(
        (SUM(o.total_amount) / (SELECT SUM(total_amount) FROM orders WHERE order_status = 'Completed')) * 100,
        2
    ) AS revenue_contribution_pct
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_status = 'Completed'
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY customer_revenue DESC
LIMIT 10;