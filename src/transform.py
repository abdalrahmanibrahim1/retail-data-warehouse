import pandas as pd
import src.validate as validate
from src.extract import extract_all
from datetime import date

def build_dim_customer(valid_customers_df):
    dim_customer = valid_customers_df.copy().reset_index(drop=True)
    dim_customer.insert(0, "customer_key", range(1, len(dim_customer) + 1))

    return dim_customer

def build_dim_product(valid_products_df):
    dim_product = valid_products_df.copy().reset_index(drop=True)
    dim_product.insert(0, "product_key", range(1, len(dim_product) + 1))
    
    dim_product = dim_product.drop(columns =["base_price", "base_cost"])
    return dim_product

def build_dim_store(valid_stores_df):
    dim_stores = valid_stores_df.copy().reset_index(drop=True)
    dim_stores.insert(0, "store_key", range(1, len(dim_stores) + 1))

    return dim_stores

def build_dim_date():
    start_date = date(2025, 1, 1)
    end_date = date(2026, 12, 31)
    
    date_list = pd.date_range(start=start_date, end=end_date, freq="D")

    dim_date = pd.DataFrame({"full_date": date_list}) 

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
    sales = valid_sales_df.copy()

    sales_with_customer_key = sales.merge(
        dim_customer[["customer_id", "customer_key"]],
        on = "customer_id",
        how = "left"
    )
    
    sales_with_customer_key["customer_key"] = sales_with_customer_key["customer_key"].astype("int")

    sales_with_product_key = sales_with_customer_key.merge(
        dim_product[["product_id", "product_key"]],
        on = "product_id",
        how = "left"
    )

    sales_with_product_key["product_key"] = sales_with_product_key["product_key"].astype("int")


    sales_with_store_key = sales_with_product_key.merge(
        dim_store[["store_id", "store_key"]],
        on = "store_id",
        how = "left"
    )

    sales_with_store_key["store_key"] = sales_with_store_key["store_key"].astype("int")

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

    fact_sales = sales_with_date_key[
        ["sale_id", "customer_key", "product_key", "store_key", "date_key", "quantity", "unit_price", "unit_cost"]
    ].copy()
    
    fact_sales["quantity"] = fact_sales["quantity"].astype("int")
    fact_sales["unit_price"] = pd.to_numeric(fact_sales["unit_price"])
    fact_sales["unit_cost"] = pd.to_numeric(fact_sales["unit_cost"])

    fact_sales["revenue"] = fact_sales["unit_price"]* fact_sales["quantity"]
    fact_sales["profit"] = fact_sales["revenue"] - (fact_sales["unit_cost"] * fact_sales["quantity"])

    fact_sales.insert(0, "sale_key", range(1, len(fact_sales) + 1))

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


if __name__ == "__main__":
    data = extract_all()
    valid_data, invalid_data = validate.validate_all(
        data["customers"],
        data["products"],
        data["stores"],
        data["sales"]
    )

    transformed_data = transform_all(valid_data)

    for table_name, df in transformed_data.items():
        print(table_name)
        print(df.head())