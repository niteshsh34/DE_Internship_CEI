import pandas as pd
from datetime import datetime

# Read Orders CSV
orders = pd.read_csv("../data/raw/orders.csv")

print("=" * 50)
print("ORDERS DATA")
print("=" * 50)

print("\nFirst 5 Rows:")
print(orders.head())

print("\nColumns:")
print(orders.columns.tolist())

print("\nTotal Rows:", len(orders))

print("\nMissing Values:")
print(orders.isnull().sum())

print("\nData Types:")
print(orders.dtypes)

print("\n" + "=" * 50)
print("Cleaning Orders...")
print("=" * 50)


# Handle Missing Customer IDs
missing_customer = orders["customer_id"].isnull().sum()
print(f"Missing Customer IDs : {missing_customer}")

orders["customer_id"] = (
    orders["customer_id"]
    .fillna(-1)
    .astype(int)
)


# Date Cleaning (Using Pandas)
wrong_dates = 0
future_dates = 0

original_dates = orders["order_date"].copy()

# Automatically parse mixed date formats
orders["order_date"] = pd.to_datetime(
    orders["order_date"],
    format="mixed",
    errors="coerce"
)

# Count invalid dates
invalid_dates = orders["order_date"].isna().sum()

# Count future dates
future_dates = (orders["order_date"] > pd.Timestamp.now()).sum()

# Count rows whose format changed
wrong_dates = (original_dates != orders["order_date"].dt.strftime("%Y-%m-%d %H:%M:%S")).sum()

# Remove invalid dates
orders = orders.dropna(subset=["order_date"])

# Convert to standard format
orders["order_date"] = orders["order_date"].dt.strftime("%Y-%m-%d %H:%M:%S")

# Save Cleaned File
orders.to_csv(
    "../data/cleaned/orders_clean.csv",
    index=False
)

print("\nCleaning Finished")
print(f"Wrong Date Formats Fixed : {wrong_dates}")
print(f"Future Dates Found      : {future_dates}")
print(f"Invalid Dates Removed   : {invalid_dates}")

print("\nCleaned file saved successfully!")