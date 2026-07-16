import sqlite3
import pandas as pd

# Connect to Database
conn = sqlite3.connect("ecommerce.db")

print("Connected to SQLite")

# Read Cleaned CSV Files
customers = pd.read_csv("../data/raw/customers.csv")  # no cleaning yet
products = pd.read_csv("../data/cleaned/products_clean.csv")
orders = pd.read_csv("../data/cleaned/orders_clean.csv")
order_items = pd.read_csv("../data/raw/order_items.csv")  # no cleaning yet

# Load into Database
customers.to_sql(
    "customers",
    conn,
    if_exists="replace",
    index=False
)

products.to_sql(
    "products",
    conn,
    if_exists="replace",
    index=False
)

orders.to_sql(
    "orders",
    conn,
    if_exists="replace",
    index=False
)

order_items.to_sql(
    "order_items",
    conn,
    if_exists="replace",
    index=False
)

print("All tables loaded successfully!")

conn.close()
print("Database Closed")