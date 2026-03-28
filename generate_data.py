import pymysql
import random
from faker import Faker
from datetime import datetime, timedelta

# 连接数据库
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',      
    database='ecommerce',
    charset='utf8mb4'
)
cursor = conn.cursor()

fake = Faker('zh_CN')  # 使用中文数据

# -------------------- 1. 插入 10 万用户 --------------------
def insert_users(n=100000):
    sql = "INSERT INTO users (username, email, register_time) VALUES (%s, %s, %s)"
    batch_size = 5000
    data = []
    for i in range(n):
        username = fake.user_name()
        email = fake.email()
        register_time = fake.date_time_between(start_date='-2y', end_date='now')
        data.append((username, email, register_time))
        if len(data) >= batch_size:
            cursor.executemany(sql, data)
            conn.commit()
            data = []
            print(f"已插入 {i+1} 个用户")
    if data:
        cursor.executemany(sql, data)
        conn.commit()
    print(f"用户插入完成，共 {n} 条")

# -------------------- 2. 插入 1000 种商品 --------------------
def insert_products(n=1000):
    sql = "INSERT INTO products (product_name, category, price) VALUES (%s, %s, %s)"
    categories = ['电子产品', '服装', '食品', '图书', '家居', '美妆']
    data = []
    for i in range(n):
        name = f"{fake.word()}_{i}"   # 避免重名
        category = random.choice(categories)
        price = round(random.uniform(10, 2000), 2)
        data.append((name, category, price))
    cursor.executemany(sql, data)
    conn.commit()
    print(f"商品插入完成，共 {n} 条")

# -------------------- 3. 插入订单和明细 --------------------
def insert_orders_and_items(n_orders=100000):  # 10 万订单
    # 获取所有 user_id
    cursor.execute("SELECT user_id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]
    # 获取所有商品
    cursor.execute("SELECT product_id, price FROM products")
    products = cursor.fetchall()

    orders_data = []
    items_data = []  # 暂存每个订单的明细（待填充 order_id）

    for i in range(n_orders):
        if i % 10000 == 0:
            print(f"生成订单进度: {i}/{n_orders}")

        user_id = random.choice(user_ids)
        order_time = fake.date_time_between(start_date='-2y', end_date='now')
        # 随机生成 1~5 件商品
        num_items = random.randint(1, 5)
        chosen_products = [random.choice(products) for _ in range(num_items)]
        total = 0
        items_for_order = []
        for prod_id, prod_price in chosen_products:
            qty = random.randint(1, 3)
            total += prod_price * qty
            items_for_order.append((prod_id, qty, prod_price))
        orders_data.append((user_id, order_time, total))
        items_data.append(items_for_order)

    # 批量插入订单
    cursor.executemany(
        "INSERT INTO orders (user_id, order_time, total_amount, status) VALUES (%s, %s, %s, 1)",
        orders_data
    )
    conn.commit()
    print("订单插入完成，开始插入明细...")

    # 获取这批订单的自增ID范围
    cursor.execute("SELECT LAST_INSERT_ID()")
    last_id = cursor.fetchone()[0]
    first_id = last_id - len(orders_data) + 1

    # 批量插入明细
    item_sql = "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)"
    batch_items = []
    for idx, items in enumerate(items_data):
        order_id = first_id + idx
        for prod_id, qty, price in items:
            batch_items.append((order_id, prod_id, qty, price))
        if len(batch_items) >= 5000:
            cursor.executemany(item_sql, batch_items)
            conn.commit()
            batch_items = []
    if batch_items:
        cursor.executemany(item_sql, batch_items)
        conn.commit()
    print(f"订单及明细插入完成，共 {n_orders} 个订单")

# 执行
    if __name__ == '__main__':
    # 1. 插入用户（10万）
    insert_users(100000)
    # 2. 插入商品（1000）
    insert_products(1000)
    # 3. 插入订单和明细
    insert_orders_and_items(100000)   
    conn.close()
