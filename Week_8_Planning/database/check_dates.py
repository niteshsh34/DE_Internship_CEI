import sqlite3

conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

cursor.execute("""
SELECT
MIN(order_date),
MAX(order_date)
FROM orders;
""")

print(cursor.fetchone())

conn.close()