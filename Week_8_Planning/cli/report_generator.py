import sqlite3
from datetime import datetime, timedelta
# Connect Database
conn = sqlite3.connect("../database/ecommerce.db")
cursor = conn.cursor()

print("=" * 50)
print("E-Commerce Report Generator")
print("=" * 50)

print("\nSelect Report Type")
print("1. Daily")
print("2. Weekly")
print("3. Monthly")

choice = input("\nEnter Choice : ")

start_date = input("Enter Start Date (YYYY-MM-DD): ")
end_date = input("Enter End Date (YYYY-MM-DD): ")

start = datetime.strptime(start_date, "%Y-%m-%d")
end = datetime.strptime(end_date, "%Y-%m-%d")

days = (end - start).days

previous_end = start - timedelta(days=1)
previous_start = previous_end - timedelta(days=days) 
print("\nGenerating Report...")

query = """
SELECT
COUNT(DISTINCT o.order_id),
ROUND(SUM(oi.quantity *oi.unit_price *(1-oi.discount_percent/100.0)),2),
COUNT(DISTINCT o.customer_id)
FROM orders o
JOIN order_items oi
ON o.order_id=oi.order_id
WHERE
    date(o.order_date)
    BETWEEN date(?) AND date(?)
    AND oi.quantity>0;
"""

cursor.execute(query,(start_date,end_date))
result=cursor.fetchone()

print("\n==============================")

print(f"Total Orders      : {result[0]}")
print(f"Total Revenue     : ₹ {result[1]}")
print(f"Unique Customers  : {result[2]}")
print("==============================")
print("\nTop 3 Products")

query = """
SELECT
    p.product_name,
    SUM(oi.quantity) AS total_quantity
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE
    date(o.order_date)
    BETWEEN date(?)
    AND date(?)
AND oi.quantity > 0
GROUP BY p.product_name
ORDER BY total_quantity DESC
LIMIT 3;
"""

cursor.execute(query, (start_date, end_date))
products = cursor.fetchall()

for i, product in enumerate(products, start=1):
    print(f"{i}. {product[0]} ({product[1]} units)")

# revenue query 
revenue_query = """
SELECT
ROUND(
SUM(oi.quantity * oi.unit_price * (1-oi.discount_percent/100.0)),2)
FROM orders o
JOIN order_items oi ON o.order_id=oi.order_id
WHERE date(o.order_date) BETWEEN date(?) AND date(?) AND oi.quantity>0;
"""

# Current Revenue
cursor.execute(
    revenue_query,
    (start_date, end_date)
)

current = cursor.fetchone()[0] or 0
# Previous Revenue
cursor.execute(
    revenue_query,
    (
        previous_start.strftime("%Y-%m-%d"),
        previous_end.strftime("%Y-%m-%d")
    )
)

previous = cursor.fetchone()[0] or 0
# Percentage Change
if previous == 0:
    change = 0
else:
    change = round(((current - previous) / previous) * 100,2)

print("\nRevenue Comparison")
print(f"Current Revenue : ₹ {current}")
print(f"Previous Revenue : ₹ {previous}")
print(f"Change : {change}%")