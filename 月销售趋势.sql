SELECT 
    DATE_FORMAT(order_time, '%Y-%m') AS month,
    SUM(total_amount) AS revenue
FROM orders
WHERE status = 1
GROUP BY month
ORDER BY month
LIMIT 10;