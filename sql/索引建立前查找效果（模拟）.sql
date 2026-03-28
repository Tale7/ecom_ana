EXPLAIN FORMAT=tree
SELECT 
    p.product_name,
    SUM(oi.quantity) AS total_sold
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o IGNORE INDEX (idx_status_time) ON oi.order_id = o.order_id
WHERE o.status = 1
GROUP BY p.product_name
ORDER BY total_sold DESC
LIMIT 10;