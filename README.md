# Retail Data Warehouse Pipeline

A production-style retail data warehouse project built with Python, pandas, PostgreSQL, SQL, pytest, and Docker.

This project simulates a retail business with customers, products, stores, and sales. It extracts source CSV files, validates data quality, transforms the data into a star schema, loads the warehouse into PostgreSQL, runs integrity tests, and generates reporting outputs as CSV and Markdown files.

---

## Project Overview

The goal of this project is to demonstrate a complete data engineering workflow:

1. Generate realistic synthetic retail source data.
2. Inject intentionally invalid rows to test validation rules.
3. Extract raw CSV files.
4. Validate schema, IDs, business rules, foreign keys, dates, and numeric values.
5. Transform valid data into a star schema.
6. Load dimension and fact tables into PostgreSQL.
7. Validate warehouse integrity with tests.
8. Generate business reports from the warehouse.
9. Run the full pipeline locally or with Docker Compose.

---

## Tech Stack

* Python
* pandas
* PostgreSQL
* psycopg2
* pytest
* Faker
* python-dotenv
* Docker
* Docker Compose

---

## Project Structure

```text
retail-data-warehouse/
├── data/
│   ├── customers.csv
│   ├── products.csv
│   ├── stores.csv
│   └── sales.csv
│
├── reports/
│   ├── warehouse_report.md
│   └── generated CSV report files
│
├── scripts/
│   └── generate_data.py
│
├── src/
│   ├── extract.py
│   ├── validate.py
│   ├── transform.py
│   ├── load.py
│   ├── report.py
│   └── main.py
│
├── tests/
│   ├── test_validate.py
│   ├── test_transform.py
│   └── test_integrity.py
│
├── schema.sql
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example
├── .gitignore
└── README.md
```

---

## Data Sources

The project uses four source CSV files:

```text
data/customers.csv
data/products.csv
data/stores.csv
data/sales.csv
```

These files can be generated using:

```bash
python -m scripts.generate_data
```

The generated source data includes both valid and intentionally invalid rows. Invalid rows are included on purpose so the validation layer can demonstrate rejection of bad data.

---

## Source Schema Assumption

This project expects each source CSV file to have the exact expected column names in the exact expected column order.

For example, `customers.csv` must use this structure:

```text
customer_id, customer_name, customer_city, customer_segment
```

The pipeline intentionally checks column order, not just column names. This is because CSV files are treated as fixed-format source extracts. If a source system changes the structure or column order unexpectedly, the pipeline should fail fast instead of silently processing incorrect data.

This assumption is enforced in the validation layer.

---

## Expected Source Schemas

### customers.csv

```text
customer_id
customer_name
customer_city
customer_segment
```

### products.csv

```text
product_id
product_name
category
brand
base_price
base_cost
```

### stores.csv

```text
store_id
store_name
store_city
```

### sales.csv

```text
sale_id
customer_id
product_id
store_id
sale_date
quantity
unit_price
unit_cost
```

---

## Pipeline Architecture

```text
CSV Source Files
      |
      v
Extraction Layer
      |
      v
Validation Layer
      |
      v
Transformation Layer
      |
      v
PostgreSQL Star Schema Warehouse
      |
      v
Reporting Layer
```

The pipeline is orchestrated from:

```bash
python -m src.main
```

---

## Pipeline Stages

### 1. Data Generation

`scripts/generate_data.py` creates synthetic retail data for:

* Customers
* Products
* Stores
* Sales

It also injects invalid rows to test validation rules, including:

* Missing IDs
* Incorrect ID formats
* Duplicate IDs
* Missing names
* Invalid cities
* Invalid customer segments
* Invalid product categories
* Non-numeric prices/costs
* Negative or zero prices/costs
* Invalid sale dates
* Invalid foreign keys
* Invalid quantities
* Cost greater than price

---

### 2. Extraction

`src/extract.py` reads the raw CSV files from the `data/` directory and returns them as pandas DataFrames.

The extraction layer returns a dictionary:

```python
{
    "customers": customers_df,
    "products": products_df,
    "stores": stores_df,
    "sales": sales_df,
}
```

---

### 3. Validation

`src/validate.py` validates each source table and separates rows into valid and invalid DataFrames.

Validation is sequential. Rows that fail one rule are removed from the valid dataset before the next rule is checked. This prevents the same row from being counted as invalid multiple times.

Dimension tables are validated first:

```text
customers
products
stores
```

Sales are validated last because each sale must reference valid customers, products, and stores.

Main validation rules include:

* Required schema and exact column order
* Valid ID format
* No duplicate IDs after the first occurrence
* Required names and brands
* Allowed cities
* Allowed customer segments
* Allowed product categories
* Positive numeric price and cost values
* Cost must be less than or equal to price
* Valid sale dates within the warehouse date range
* Positive whole-number quantities
* Valid foreign-key references from sales to dimensions

---

### 4. Transformation

`src/transform.py` transforms validated source data into a star schema.

The transformation layer creates:

```text
dim_customer
dim_product
dim_store
dim_date
fact_sales
```

Surrogate keys are created for dimension tables:

```text
customer_key
product_key
store_key
date_key
```

The sales fact table maps source IDs to warehouse surrogate keys and calculates:

```text
revenue = quantity * unit_price
profit = revenue - (quantity * unit_cost)
```

---

## Warehouse Schema

The warehouse uses a star schema.

### dim_customer

```text
customer_key
customer_id
customer_name
customer_city
customer_segment
```

### dim_product

```text
product_key
product_id
product_name
category
brand
```

### dim_store

```text
store_key
store_id
store_name
store_city
```

### dim_date

```text
date_key
full_date
year
quarter
month
day
weekday
```

The date dimension covers:

```text
2025-01-01 through 2026-12-31
```

### fact_sales

```text
sale_key
sale_id
customer_key
product_key
store_key
date_key
quantity
revenue
profit
```

The grain of `fact_sales` is one row per sale transaction.

---

## Loading Strategy

This project uses a full-refresh warehouse loading strategy. On each run, warehouse tables are truncated and rebuilt from validated source CSV files inside a single database transaction.

The loading process:

1. Creates warehouse tables if they do not already exist.
2. Truncates existing warehouse tables.
3. Loads dimension tables.
4. Loads the fact table.
5. Commits the transaction if all loads succeed.
6. Rolls back the transaction if any load fails.

Dimension tables are loaded before the fact table because `fact_sales` depends on dimension surrogate keys.

Future improvement: incremental loading using staging tables, upserts, and duplicate detection on sale_id.

---

## Reporting Layer

`src/report.py` queries the PostgreSQL warehouse and generates reporting outputs.

The reporting layer produces:

* Detailed CSV files for analysis tools
* A Markdown summary report for human review

CSV outputs are kept machine-readable. Numeric values remain raw so they can be used in Excel, Power BI, Tableau, or pandas.

Markdown output is formatted for readability and GitHub preview.

Generated reports include:

```text
warehouse_summary.csv
revenue_by_product_category.csv
top_5_products_by_revenue.csv
sales_by_store_city.csv
revenue_by_customer_segment.csv
monthly_revenue_trend.csv
category_city_segment_performance.csv
category_profit_margin_ranking.csv
customer_segment_average_sale_ranking.csv
monthly_revenue_growth.csv
monthly_category_revenue_trend.csv
electronics_monthly_revenue_growth.csv
warehouse_report.md
```

---

## Example Business Questions Answered

The reporting layer can answer questions such as:

* What is total revenue and profit?
* Which product categories generate the most revenue?
* What are the top 5 products by revenue?
* Which store cities perform best?
* Which customer segments generate the most revenue?
* How does revenue trend by month?
* Which categories have the highest profit margins?
* Which customer segments have the highest average sale value?
* How is revenue growing month over month?
* How does a specific category grow month over month?

---

## Testing

The project includes tests for:

### Validation Logic

`tests/test_validate.py`

Tests whether invalid source rows are rejected correctly and valid extracted data passes the full validation workflow.

### Transformation Logic

`tests/test_transform.py`

Tests whether dimension and fact tables are built correctly, including:

* Surrogate keys
* Date keys
* Fact table keys
* Revenue calculation
* Profit calculation
* Full transformation output

### Warehouse Integrity

`tests/test_integrity.py`

Tests the loaded PostgreSQL warehouse, including:

* Required tables exist
* Warehouse tables are not empty
* `dim_date` has the expected 730 rows
* `fact_sales` has no orphan foreign keys
* Fact measures are valid

Run tests with:

```bash
python -m pytest
```

---

## Local Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd retail-data-warehouse
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example`.

Example:

```env
DB_HOST=localhost
DB_NAME=retail_data_warehouse
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432
```

### 5. Generate source data

```bash
python -m scripts.generate_data
```

### 6. Run the full pipeline

```bash
python -m src.main
```

### 7. Run tests

```bash
python -m pytest
```

---

## Docker Setup

This project can also run with Docker Compose.

Docker Compose starts:

1. A PostgreSQL container
2. A Python app container that runs the full pipeline

Run:

```bash
docker compose up --build
```

Inside Docker Compose, the Python container connects to PostgreSQL using:

```env
DB_HOST=db
```

This is different from local execution, where `DB_HOST` is usually `localhost`.

The Dockerized pipeline:

1. Starts PostgreSQL
2. Waits for the database to become healthy
3. Runs the Python pipeline
4. Loads the warehouse
5. Generates reports
6. Exits after successful completion

---

## Logging

The project uses Python logging instead of print statements for pipeline execution.

Example pipeline log flow:

```text
Starting retail data warehouse pipeline
Extracting source data
Validating source data
Transforming valid data into star schema tables
Loading transformed data into PostgreSQL warehouse
Warehouse load committed successfully
Generating warehouse report files
Pipeline completed successfully
```

The logger includes module names so logs can show which part of the project produced each message.

---

## Generated Reports

After running the pipeline, report files are written to:

```text
reports/
```

The main human-readable report is:

```text
reports/warehouse_report.md
```

Detailed CSV outputs are also written to the same folder.

Depending on repository settings, generated report outputs may be excluded from version control because they can be regenerated by running the pipeline.

---

## Environment Variables

The project expects the following environment variables:

```env
DB_HOST=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_PORT=
```

For local execution, use `.env`.

For Docker execution, these values are provided through `docker-compose.yml`.

---

## Full Refresh vs Incremental Loading

This project currently uses a full-refresh loading approach.

A full refresh is simple, reliable, and appropriate for this project because the dataset is small and generated from CSV source files.

Current behavior:

```text
TRUNCATE warehouse tables
Load validated dimensions
Load validated fact table
Commit transaction
```

If a failure occurs, the transaction is rolled back to prevent a partially loaded warehouse.

Future improvement:

```text
Use staging tables
Detect duplicate sale_id values
Apply inserts/updates with upserts
Load only new or changed records
Track batch load timestamps
Add audit tables
```

---

## Future Improvements

Potential future improvements include:

* Incremental loading with staging tables and upserts
* Duplicate detection on `sale_id`
* Invalid-row export to rejection reports
* Audit table for pipeline run history
* Load timestamps and batch IDs
* Data quality summary report
* Excel workbook output with multiple report sheets
* HTML dashboard
* Power BI or Tableau dashboard
* Slowly Changing Dimension Type 2 support for customer or product changes
* CI pipeline to run tests automatically
* More advanced Docker setup for separate data generation and pipeline execution commands

---

## Key Skills Demonstrated

This project demonstrates:

* Data extraction from CSV sources
* Schema validation
* Data quality validation
* Referential integrity validation
* Star schema design
* Surrogate key generation
* Fact and dimension modeling
* PostgreSQL loading
* Transaction handling
* Rollback on failure
* SQL reporting
* Window functions
* CSV and Markdown report generation
* pytest unit and integration testing
* Docker Compose orchestration
* Logging-based pipeline execution
* End-to-end data pipeline orchestration

---

## How to Run Everything

Local:

```bash
python -m scripts.generate_data
python -m src.main
python -m pytest
```

Docker:

```bash
docker compose up --build
```

---

## Project Status

Completed:

* Synthetic data generation
* Extraction layer
* Validation layer
* Transformation layer
* PostgreSQL warehouse loading
* Full-refresh transaction strategy
* Reporting layer
* CSV and Markdown report generation
* Pipeline orchestration
* Logging
* Tests
* Docker Compose setup

Planned future improvement:

* Incremental loading with staging tables, upserts, and duplicate detection on `sale_id`

```
```
