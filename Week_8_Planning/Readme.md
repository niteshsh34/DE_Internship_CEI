# E-Commerce Order Analytics System

## Project Overview

This project simulates a real-world Data Engineering ETL pipeline for an e-commerce platform.
 The system generates, cleans, validates, stores, and analyzes order data using Python, SQLite, and SQL. It demonstrates data quality checks, SQL analytics, and report generation.

---

## Tech Stack

- Python
- Pandas
- SQLite
- SQL
- VS Code
---

## Project Structure

```
ECommerce_Order_Analytics
│
├── data
│   ├── raw
│   └── cleaned
│
├── scripts
│   ├── clean_orders.py
│   ├── clean_products.py
│   ├── validate_emails.py
│   ├── referential_integrity.py
│
├── database
│   ├── ecommerce.db
│   ├── load_data.py
│
├── sql
│   ├── basic_queries.sql
│   ├── intermediate_queries.sql
│   └── advanced_queries.sql
│
├── cli
│   └── report_generator.py
│
├── reports
│
├── tests
│
└── README.md
```

---

## Dataset

The project contains four datasets.

### customers.csv
- Customer Details
- Invalid email records added intentionally

### products.csv
- Product information
- Mixed case names
- Extra spaces

### orders.csv
- Order details
- Missing Customer IDs
- Multiple date formats

### order_items.csv
- Product level order details
- Negative quantity for returns
- Discount percentage

---

## ETL Pipeline

### Extract

- Read raw CSV files using Pandas.

### Transform

Performed data cleaning:

- Fixed multiple date formats
- Filled missing Customer IDs
- Removed invalid dates
- Normalized product names
- Validated email addresses
- Checked referential integrity

### Load

- Loaded cleaned data into SQLite database.

---

## SQL Analysis

Implemented SQL queries covering

### Basic

- Revenue by Category
- Top Customers
- Monthly Order Count

### Intermediate

- Customers without Delivered Orders
- Products with More Returns than Purchases
- Return Rate by Category

### Advanced

- Running Totals
- DENSE_RANK()
- LAG()
- LEAD()
- Multiple CTEs
- NTILE()
- Year-over-Year Analysis
- FIRST_VALUE()
- LAST_VALUE()
- CUME_DIST()
- Cohort Analysis
- Window Functions

---

## CLI Report Generator

The application allows users to

- Select report type
- Enter date range
- Generate sales summary
- Display total revenue
- Display total orders
- Display unique customers
- Display top products
- Compare revenue with previous period

---

## Edge Case Testing

Tested scenarios including

- Invalid Order IDs
- Discount greater than 100%
- Zero Quantity
- Future Order Dates

---

## Learning Outcomes

- ETL Pipeline Development
- Data Cleaning
- Data Validation
- SQL Analytics
- Window Functions
- Database Design
- Business Reporting
