WITH user_orders AS (
    SELECT user_id, COUNT(*) AS order_count
    FROM orders
    WHERE status = 1
    GROUP BY user_id
)
SELECT 
    COUNT(CASE WHEN order_count >= 2 THEN 1 END) AS repeat_users,
    COUNT(*) AS total_users,
    ROUND(COUNT(CASE WHEN order_count >= 2 THEN 1 END) * 100.0 / COUNT(*), 2) AS repeat_rate
FROM user_orders;
