import pandas as pd
import re

# Read Customers CSV
customers = pd.read_csv("../data/raw/customers.csv")

print("=" * 50)
print("EMAIL VALIDATION")
print("=" * 50)

# Email Validation Function
def is_valid_email(email):
    if pd.isna(email):
        return False
    email = str(email).strip()
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(pattern, email) is not None

# Find Invalid Emails
invalid_customers = customers[
    ~customers["email"].apply(is_valid_email)
]

print(f"\nTotal Customers : {len(customers)}")
print(f"Invalid Emails  : {len(invalid_customers)}")

# Save Invalid Emails
invalid_customers.to_csv(
    "../reports/invalid_emails.csv",
    index=False
)

print("\nInvalid email list saved.")

# Display Invalid Emails
if len(invalid_customers) > 0:
    print("\nInvalid Customer IDs:")
    print(invalid_customers[["customer_id", "email"]])