import pandas as pd

# Read CSV Files
orders = pd.read_csv("../data/raw/orders.csv")
order_items = pd.read_csv("../data/raw/order_items.csv")

print("=" * 50)
print("REFERENTIAL INTEGRITY CHECK")
print("=" * 50)

# Valid Order IDs
valid_order_ids = set(orders["order_id"])

# Find Invalid References
invalid_rows = order_items[
    ~order_items["order_id"].isin(valid_order_ids)
]

print(f"\nTotal Order Items : {len(order_items)}")
print(f"Invalid References : {len(invalid_rows)}")

# Save Report
invalid_rows.to_csv(
    "../reports/invalid_order_items.csv",
    index=False
)

print("\nReport saved successfully!")

# Show Invalid Records
if len(invalid_rows) > 0:
    print("\nInvalid Order Items:")
    print(invalid_rows)
else:
    print("\nNo referential integrity issues found.")