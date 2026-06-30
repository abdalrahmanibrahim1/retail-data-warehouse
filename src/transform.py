import pandas as pd
from datetime import date

def build_dim_customer(valid_customers_df):
    """
    Build the customer dimension table from validated customer source data.

    A warehouse surrogate key is added so fact tables can reference customers
    independently of the original source customer_id.
    """
    dim_customer = valid_customers_df.copy().reset_index(drop=True)
    dim_customer.insert(0, "customer_key", range(1, len(dim_customer) + 1))

    return dim_customer

def build_dim_product(valid_products_df):
    """
    Build the product dimension table from validated product source data.

    A warehouse surrogate key is added, and base_price/base_cost are removed
    because transactional price and cost values belong in the sales fact logic.
    """
    dim_product = valid_products_df.copy().reset_index(drop=True)
    dim_product.insert(0, "product_key", range(1, len(dim_product) + 1))
    
    dim_product = dim_product.drop(columns =["base_price", "base_cost"])
    return dim_product

def build_dim_store(valid_stores_df):
    """
    Build the store dimension table from validated store source data.

    A warehouse surrogate key is added so fact tables can reference stores
    independently of the original source store_id.
    """
    dim_store = valid_stores_df.copy().reset_index(drop=True)
    dim_store.insert(0, "store_key", range(1, len(dim_store) + 1))

    return dim_store

def build_dim_date():
    """
    Build the date dimension table used by the sales fact table.

    The date range is fixed to 2025-01-01 through 2026-12-31, matching the
    accepted sale_date range in validation.
    """
    start_date = date(2025, 1, 1)
    end_date = date(2026, 12, 31)
    
    date_list = pd.date_range(start=start_date, end=end_date, freq="D")

    dim_date = pd.DataFrame({"full_date": date_list}) 

    # Use YYYYMMDD as a stable integer date key for joining fact_sales to dim_date.
    dim_date["date_key"] = dim_date["full_date"].dt.strftime("%Y%m%d").astype(int)
    dim_date["year"]     = dim_date["full_date"].dt.year
    dim_date["quarter"]  = dim_date["full_date"].dt.quarter
    dim_date["month"]    = dim_date["full_date"].dt.month
    dim_date["day"]      = dim_date["full_date"].dt.day

    dim_date["weekday"] = dim_date["full_date"].dt.day_name()

    column_order =["date_key", "full_date", "year", "quarter", "month", "day","weekday"]
    dim_date = dim_date[column_order]

    return dim_date

def build_fact_sales(valid_sales_df, dim_customer, dim_product, dim_store, dim_date):
    """
    Build the sales fact table by mapping validated sales rows to warehouse dimension keys.

    Source IDs from the sales data are replaced with surrogate keys from the customer,
    product, store, and date dimensions. The function also calculates revenue and
    profit measures, then returns the final fact_sales table at the sale transaction grain.
    """
    sales = valid_sales_df.copy()

    # Map source customer_id to warehouse customer_key.
    sales_with_customer_key = sales.merge(
        dim_customer[["customer_id", "customer_key"]],
        on = "customer_id",
        how = "left"
    )
    
    sales_with_customer_key["customer_key"] = sales_with_customer_key["customer_key"].astype("int")

    # Map source product_id to warehouse product_key.
    sales_with_product_key = sales_with_customer_key.merge(
        dim_product[["product_id", "product_key"]],
        on = "product_id",
        how = "left"
    )

    sales_with_product_key["product_key"] = sales_with_product_key["product_key"].astype("int")

    # Map source store_id to warehouse store_key.
    sales_with_store_key = sales_with_product_key.merge(
        dim_store[["store_id", "store_key"]],
        on = "store_id",
        how = "left"
    )

    sales_with_store_key["store_key"] = sales_with_store_key["store_key"].astype("int")

    # Normalize sale dates and dimension dates to the same format before joining.
    sales_with_store_key["sale_date"] = pd.to_datetime(
        sales_with_store_key["sale_date"]
    ).dt.strftime("%Y-%m-%d")

    dim_date_lookup = dim_date.copy()

    dim_date_lookup["full_date"] = pd.to_datetime(
        dim_date_lookup["full_date"]
    ).dt.strftime("%Y-%m-%d")


    sales_with_date_key = sales_with_store_key.merge(
        dim_date_lookup[["date_key","full_date"]],
        left_on = "sale_date",
        right_on = "full_date",
        how = "left"
    )

    # Keep only columns needed to build the fact table.
    fact_sales = sales_with_date_key[
        ["sale_id", "customer_key", "product_key", "store_key", "date_key", "quantity", "unit_price", "unit_cost"]
    ].copy()
    
    fact_sales["quantity"] = fact_sales["quantity"].astype("int")
    fact_sales["date_key"] = fact_sales["date_key"].astype("int")
    fact_sales["unit_price"] = pd.to_numeric(fact_sales["unit_price"])
    fact_sales["unit_cost"] = pd.to_numeric(fact_sales["unit_cost"])

    # Calculate fact measures from transaction-level quantity, price, and cost.
    fact_sales["revenue"] = fact_sales["unit_price"]* fact_sales["quantity"]
    fact_sales["profit"] = fact_sales["revenue"] - (fact_sales["unit_cost"] * fact_sales["quantity"])

    fact_sales.insert(0, "sale_key", range(1, len(fact_sales) + 1))

    # Return the final fact table shape expected by the warehouse schema.
    fact_sales = fact_sales[
        [
            "sale_key",
            "sale_id",
            "customer_key", 
            "product_key", 
            "store_key", 
            "date_key", 
            "quantity", 
            "revenue", 
            "profit"
        ]
    ]    

    return fact_sales

def transform_all(valid_data):
    """
    Transform all validated source tables into warehouse-ready dimension and fact tables.

    Dimension tables are built first so fact_sales can map source IDs to warehouse
    surrogate keys.
    """
    dim_customer = build_dim_customer(valid_data["customers"])
    dim_product = build_dim_product(valid_data["products"])
    dim_store = build_dim_store(valid_data["stores"])
    dim_date = build_dim_date()
    fact_sales = build_fact_sales(valid_data["sales"], dim_customer, dim_product, dim_store, dim_date)

    transformed_data ={
        "dim_customer" : dim_customer,
        "dim_product" : dim_product, 
        "dim_store" : dim_store,
        "dim_date" : dim_date,
        "fact_sales" : fact_sales,
    }

    return transformed_data