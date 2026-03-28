CREATE INDEX idx_status_time ON orders(status, order_time);
-- 可选
-- CREATE INDEX idx_product ON order_items(product_id);
-- CREATE INDEX idx_order ON order_items(order_id);