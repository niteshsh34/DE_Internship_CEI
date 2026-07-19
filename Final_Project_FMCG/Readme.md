# FMCG Data Engineering Project

## Project Overview

This project is an end-to-end FMCG data engineering pipeline built using **Databricks, Apache Spark (PySpark), Delta Lake, AWS S3, and SQL**.

The project simulates a business scenario where data from a **child company ** is standardized and integrated into an existing **parent company** data model.

The child company provides customer, product, gross price, and order data. The pipeline follows the **Medallion Architecture**:

**AWS S3 → Bronze → Silver → Gold → Parent Company Gold Tables**

The parent company's own ingestion pipeline is outside the scope of this project. The project assumes that the parent Gold tables already exist.

------------------------------------------------------------------------

## Technologies Used

-   Databricks
-   Apache Spark / PySpark
-   Delta Lake
-   AWS S3
-   Spark SQL / SQL
-   Databricks Workflows / Jobs
-   Unity Catalog

------------------------------------------------------------------------

## Project Structure

``` text
0_data/
├── 1_parent_company/
│   ├── full_load/
│   └── incremental_load/
│
└── 2_child_company/
    ├── full_load/
    │   ├── customers/
    │   ├── gross_price/
    │   ├── orders/
    │   │   └── landing/
    │   └── products/
    └── incremental_load/
        └── orders/

1_codes/
├── 1_setup/
│   ├── dim_date_table_creation.ipynb
│   ├── setup_catalog.ipynb
│   └── utilities.ipynb
│
├── 2_dimension_data_processing/
│   ├── 1_customers_data_processing.ipynb
│   ├── 2_products_data_processing.ipynb
│   └── 3_pricing_data_processing.ipynb
│
└── 3_fact_data_processing/
    ├── 1_full_load_fact.ipynb
    └── 2_incremental_load_fact.ipynb

2_dashboarding/
resources/
```

------------------------------------------------------------------------

# Data Flow

``` text
Child Company CSV Files
        |
        v
      AWS S3
        |
        v
      Bronze
   (Raw Data)
        |
        v
      Silver
(Cleaned & Standardized)
        |
        v
 Child Company Gold
        |
        v
Delta Lake MERGE
        |
        v
Existing Parent Company Gold Tables
```

The main parent Gold tables used by the project are:

-   `dim_customers`
-   `dim_products`
-   `dim_gross_price`
-   `fact_orders`

The child-company Gold tables include:

-   `sb_dim_customers`
-   `sb_dim_products`
-   `sb_dim_gross_price`
-   `sb_fact_orders`

-   `dim_date` This table is generated and provides a complete calendar with every month, including months where `no` orders occurred 
------------------------------------------------------------------------
# Prerequisites
Before running the project, ensure you have:
1.  A Databricks workspace.
2.  An AWS S3 bucket accessible from Databricks.
3.  Permission to create catalogs, schemas, and Delta tables.
4.  The project notebooks imported into the Databricks workspace.
5.  Parent-company Gold tables already created/populated if you want to execute the final child-to-parent MERGE steps.

> The sample code uses the catalog name `fmcg` and S3 paths beginning with `s3://de-project-fmcg/`. Update these values if your environment uses different names.

------------------------------------------------------------------------

# Step 1: Configure AWS S3
Create an S3 bucket for the project. The example project uses:
``` text
s3://de-project-fmcg/
```
Create source folders such as:
``` text
s3://de-project-fmcg/customers/
s3://de-project-fmcg/products/
s3://de-project-fmcg/gross_price/
s3://de-project-fmcg/orders/
```
For the incremental Orders pipeline, use:
``` text
s3://de-project-fmcg/orders/landing/
s3://de-project-fmcg/orders/processed/
```
Upload the initial/full-load CSV datasets to their corresponding S3 locations.
For incremental Orders processing, upload **only newly arrived order CSV files** into:
``` text
s3://de-project-fmcg/orders/landing/
```

After successful ingestion, the pipeline moves these files to:
``` text
s3://de-project-fmcg/orders/processed/
```
This prevents the same source file from being processed repeatedly.

------------------------------------------------------------------------

# Step 2: Run Setup Notebooks
Run the notebooks inside `1_codes/1_setup/`.
## `setup_catalog.ipynb`
Creates or configures the required catalog and schemas used by theproject.
Typical logical structure:

``` text
fmcg
├── bronze
├── silver
└── gold
```
## `utilities.ipynb`
Contains reusable project configuration and variables, such as:
``` python
bronze_schema
silver_schema
gold_schema
```
The processing notebooks load these utilities using `%run`.
If the workspace path in `%run` is user-specific, update it before running the project.

## `dim_date_table_creation.ipynb`
Creates the Date dimension used for consistent time-based analysis.

Although Orders contains transaction dates, the Orders table only contains dates/months where transactions exist. The Date dimension
provides a complete time structure, including months with no sales, which is useful for monthly reporting and trend analysis.
------------------------------------------------------------------------

# Step 3: Process Dimension / Master Data

Before processing Orders, prepare the dimension/master datasets.
A recommended dependency order is:
``` text
Customers
    |
Products
    |
Gross Price
    |
Orders
```
`Products` must be available before dependent processing that needs
`product_code`, particularly Gross Price and Orders.

## `1_customers_data_processing.ipynb`
Processes customer master data.
Main operations:
-   Reads customer CSV data from S3.
-   Loads raw data into Bronze.
-   Removes duplicate `customer_id` records.
-   Trims customer names.
-   Corrects city spelling mistakes.
-   Standardizes customer-name casing.
-   Handles known missing cities.
-   Creates standardized attributes such as `customer`, `market`, `platform`, and `channel`.
-   Writes cleaned data to Silver.
-   Creates child Gold table `sb_dim_customers`.
-   Merges standardized records into parent `dim_customers`.

## `2_products_data_processing.ipynb`
Processes product master data.
Main operations:
-   Reads product CSV data from S3.
-   Loads raw data into Bronze.
-   Removes duplicate products.
-   Standardizes categories.
-   Corrects spelling issues.
-   Creates the `division` attribute.
-   Extracts product `variant`.
-   Generates a deterministic SHA-256 `product_code`.
-   Writes standardized data to Silver.
-   Creates `sb_dim_products`.
-   Merges standardized products into parent `dim_products`.
This notebook is an important dependency because Orders and Gross Price
use the cleaned Products table to map `product_id` to `product_code`.

## `3_pricing_data_processing.ipynb`

Processes gross-price data.
Main operations:
-   Reads gross-price CSV data from S3.
-   Loads raw data into Bronze.
-   Standardizes different month/date formats.
-   Validates `gross_price`.
-   Converts valid prices to numeric values.
-   Handles negative and invalid price values.
-   Joins with Silver Products to obtain `product_code`.
-   Creates `sb_dim_gross_price`.
-   Uses a window function to select the appropriate latest non-zero
    price for each product/year.
-   Merges the result into parent `dim_gross_price`.

------------------------------------------------------------------------

# Step 4: Run Initial Orders Full Load

Run:
``` text
1_codes/3_fact_data_processing/1_full_load_fact.ipynb
```
This notebook is intended for the **initial historical Orders load**.
The process is:
``` text
Historical Orders CSV
        |
        v
S3 Landing
        |
        v
Bronze Orders
        |
        v
Clean + Transform
        |
        v
Join with Silver Products
        |
        v
Silver Orders
        |
        v
Child Gold: sb_fact_orders
        |
        v
Daily-to-Monthly Aggregation
        |
        v
Parent Gold: fact_orders
```

The notebook:
1.  Reads available Orders CSV files from the S3 landing location.
2.  Adds ingestion metadata such as read timestamp, file name, and file size.
3.  Appends raw records to Bronze.
4.  Moves processed source files from `landing` to `processed`.
5.  Reads the complete Bronze Orders data.
6.  Cleans order quantity, customer ID, date formats, duplicates, and
    product ID.
7.  Joins Orders with Silver Products to obtain `product_code`.
8.  Merges the cleaned data into Silver Orders.
9.  Creates/updates child Gold `sb_fact_orders`.
10. Aggregates child daily Orders into monthly totals.
11. Merges the monthly result into parent `fact_orders`.

Run this notebook for the initial historical load or when a deliberate
full rebuild/reprocessing is required.

------------------------------------------------------------------------

# Step 5: Run Incremental Orders Load
After the initial Full Load, use:
``` text
1_codes/3_fact_data_processing/2_incremental_load_fact.ipynb
```
for future newly arrived child-company Orders.
Place the new Orders CSV file in:
``` text
s3://de-project-fmcg/orders/landing/
```
The incremental flow is:
``` text
New Orders CSV
      |
      v
Permanent Bronze + Bronze Staging
      |
      v
Process Current Batch Only
      |
      v
Permanent Silver + Silver Staging
      |
      v
Child Gold: sb_fact_orders
      |
      v
Find Affected Months
      |
      v
Recalculate Affected Months
      |
      v
Parent Gold: fact_orders
      |
      v
Drop Staging Tables
```

The staging tables temporarily contain only the current incremental batch. This avoids processing the complete historical Bronze and Silver
datasets on every run.
If no new files are available, the incremental notebook exits gracefully instead of failing the pipeline.

------------------------------------------------------------------------

# Step 6: Create a Databricks Job / Workflow
For the initial project setup, run the setup notebooks first and then execute the initial dimension and fact processing.
A typical initial execution order is:

``` text
Setup Catalog
      |
Date Dimension
      |
Customers
      |
Products
      |
Gross Price
      |
Orders Full Load
```

For regular processing, the workflow depends on which new source data has arrived.

If only new Orders arrive:
``` text
Incremental Orders
```
If new master data also arrives, process the relevant dimension data
first. For example:

``` text
Customers
    |
Products
    |
Gross Price
    |
Incremental Orders
```

This ensures Orders always has access to the latest required product mappings.

# Dashboarding

For dashboarding and reporting, a denormalized SQL view called `vw_fact_orders_enriched` is created in the Gold layer.

The view combines the `fact_orders` table with the Date, Customer, Product, and Gross Price dimension tables to provide a single business-friendly dataset.
It contains information such as:

- Date, Month, Quarter, and Year
- Customer, Market, Platform, and Channel
- Product, Category, Division, and Variant
- Sold Quantity and Product Price
- Total Sales Amount (`sold_quantity × price_inr`)

This enriched view is used as the data source for the dashboard, making it easier to create KPIs and visualizations such as total sales, monthly sales trends, product-wise sales, category-wise sales, and customer-wise sales without repeatedly writing complex joins in the dashboard layer.
