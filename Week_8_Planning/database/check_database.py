import sqlite3

conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

tables = [
    "customers",
    "products",
    "orders",
    "order_items"
]

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"{table} : {count}")

conn.close()