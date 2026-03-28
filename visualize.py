import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',   # 修改为正确密码
    database='ecommerce',
    charset='utf8mb4'
)

# 1. 销量排行
df_sales = pd.read_sql("""
    SELECT 
        p.product_name,
        SUM(oi.quantity) AS total_sold
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.status = 1
    GROUP BY p.product_name
    ORDER BY total_sold DESC
    LIMIT 10
""", conn)

# 2. 月销售趋势（强制返回字符串，并确保格式）
df_trend = pd.read_sql(r"""
    SELECT 
        DATE_FORMAT(order_time, '%Y-%m') AS month,
        SUM(total_amount) AS revenue
    FROM orders
    WHERE status = 1
    GROUP BY month
    ORDER BY month
""", conn)
# 如果 month 列是数值，转换为字符串（但仍然可能不是日期格式）
# 这里打印检查，如果还是数值，说明 SQL 有问题
print("调试：前5行数据")
print(df_trend.head())

# 确保 month 为字符串
df_trend['month'] = df_trend['month'].astype(str)

# 绘图
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.bar(df_sales['product_name'], df_sales['total_sold'], color='skyblue')
plt.xticks(rotation=45, ha='right')
plt.title('Top 10 商品销量')
plt.xlabel('商品')
plt.ylabel('销量')

plt.subplot(1, 2, 2)
plt.plot(df_trend['month'], df_trend['revenue'], marker='o', linestyle='-', color='orange')
plt.xticks(rotation=45, ha='right')
plt.title('月度销售额趋势')
plt.xlabel('月份')
plt.ylabel('销售额（元）')

plt.tight_layout()
plt.savefig('analysis_chart.png', dpi=300, bbox_inches='tight')
plt.show()

conn.close()
print("图表已生成并保存为 analysis_chart.png")