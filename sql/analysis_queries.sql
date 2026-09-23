-- ============================================================
-- SUPERMARKET SALES ANALYTICS
-- SQL Analysis Queries
-- ============================================================


-- ============================================================
-- 1. PRODUCT LINE ANALYSIS
-- Total sales, transactions and average transaction by product
-- ============================================================

SELECT
    product_line,
    COUNT(DISTINCT invoice_id) AS transactions,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(AVG(sales), 2) AS average_transaction
FROM supermarket_sales
GROUP BY product_line
ORDER BY total_sales DESC;


-- ============================================================
-- 2. BRANCH / CITY ANALYSIS
-- Compare sales performance across branches and cities
-- ============================================================

SELECT
    branch,
    city,
    COUNT(DISTINCT invoice_id) AS transactions,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(AVG(sales), 2) AS average_transaction
FROM supermarket_sales
GROUP BY branch, city
ORDER BY total_sales DESC;


-- ============================================================
-- 3. CUSTOMER TYPE ANALYSIS
-- Compare Member and Normal customers
-- ============================================================

SELECT
    customer_type,
    COUNT(DISTINCT invoice_id) AS transactions,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(AVG(sales), 2) AS average_transaction,
    SUM(quantity) AS total_quantity,
    ROUND(AVG(rating), 2) AS average_rating
FROM supermarket_sales
GROUP BY customer_type
ORDER BY total_sales DESC;


-- ============================================================
-- 4. MONTHLY SALES ANALYSIS
-- Analyze sales performance by month
-- ============================================================

SELECT
    strftime('%m', date) AS month,
    CASE strftime('%m', date)
        WHEN '01' THEN 'January'
        WHEN '02' THEN 'February'
        WHEN '03' THEN 'March'
    END AS month_name,
    COUNT(DISTINCT invoice_id) AS transactions,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(AVG(sales), 2) AS average_transaction
FROM supermarket_sales
GROUP BY month
ORDER BY month;


-- ============================================================
-- 5. PAYMENT METHOD ANALYSIS
-- Compare Cash, Ewallet and Credit Card
-- ============================================================

SELECT
    payment,
    COUNT(DISTINCT invoice_id) AS transactions,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(AVG(sales), 2) AS average_transaction,
    SUM(quantity) AS total_quantity
FROM supermarket_sales
GROUP BY payment
ORDER BY total_sales DESC;


-- ============================================================
-- 6. TIME PERIOD ANALYSIS
-- Compare Morning, Afternoon and Evening sales
-- ============================================================

SELECT
    time_period,
    COUNT(DISTINCT invoice_id) AS transactions,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(AVG(sales), 2) AS average_transaction,
    SUM(quantity) AS total_quantity
FROM supermarket_sales
GROUP BY time_period
ORDER BY total_sales DESC;