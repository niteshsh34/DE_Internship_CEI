import pandas as pd


# Read Products CSV
products = pd.read_csv("../data/raw/products.csv")


print("PRODUCT CLEANING")
print("\nTotal Products:", len(products))

# Counter
corrected_names = 0

# Clean Product Names
def clean_product_name(name):
    global corrected_names
    original = str(name)
    # Remove extra spaces
    cleaned = original.strip()
    # Remove multiple spaces between words
    cleaned = " ".join(cleaned.split())
    # Convert to Title Case
    cleaned = cleaned.title()
    if original != cleaned:
        corrected_names += 1
    return cleaned

products["product_name"] = products["product_name"].apply(clean_product_name)

# Save Cleaned File
products.to_csv(
    "../data/cleaned/products_clean.csv",
    index=False
)

print("\nCleaning Completed")
print(f"Product Names Corrected : {corrected_names}")
print("\nCleaned file saved successfully!")