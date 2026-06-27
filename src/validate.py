from src.extract import extract_all
import pandas as pd

#constants, allowed values
ALLOWED_CITIES = {"Amman", "Irbid", "Zarqa", "Aqaba", "Salt", "Madaba", "Jerash"}
ALLOWED_CUSTOMER_SEGMENTS = {"Regular", "Premium", "Student", "Business"}
ALLOWED_PRODUCT_CATEGORIES = {"Electronics", "Clothing", "Footwear", "Grocery", "Home", "Beauty", "Sports", "Books"}
ALLOWED_STORE_CITIES = {"Amman", "Irbid", "Zarqa", "Aqaba", "Salt", "Madaba", "Jerash"}

def validate_customers_schema(customers_df):
    expected_columns = ['customer_id', 'customer_name', 'customer_city', 'customer_segment']
    actual_columns = customers_df.columns.tolist()

    if actual_columns != expected_columns:
        raise ValueError(
            f"Customer schema incorrect\n"
            f"Expected: {expected_columns}\n"
            f"Received: {actual_columns}")

def validate_customer_ids(customers_df):
    # Invalid IDs are missing, badly formatted, or duplicated after the first occurrence
    customer_ids = customers_df["customer_id"].astype("string").str.strip()

    invalid_customer_ids_mask = (
        customer_ids.isna() | 
        (customer_ids== "") |
        ~customer_ids.str.match(r"^C\d{4}$", na=False) |
        customer_ids.duplicated()
    )
    
    valid_customers_df= customers_df[~invalid_customer_ids_mask].copy()
    invalid_customers_df= customers_df[invalid_customer_ids_mask].copy()
    
    return valid_customers_df, invalid_customers_df

def validate_customer_names(customers_df):
    customer_names = customers_df["customer_name"].astype("string").str.strip()

    invalid_customer_names_mask = (
        customer_names.isna() |
        (customer_names=="")
    )

    valid_customers_df= customers_df[~invalid_customer_names_mask].copy()
    invalid_customers_df= customers_df[invalid_customer_names_mask].copy()

    return valid_customers_df, invalid_customers_df

def validate_customer_cities(customers_df):
    customer_cities = customers_df["customer_city"].astype("string").str.strip()
    invalid_customer_city_mask = ~customer_cities.isin(ALLOWED_CITIES)
    
    valid_customers_df = customers_df[~invalid_customer_city_mask].copy()
    invalid_customers_df = customers_df[invalid_customer_city_mask].copy()

    return valid_customers_df, invalid_customers_df

def validate_customer_segments(customers_df):
    customer_segments = customers_df["customer_segment"].astype("string").str.strip()
    invalid_customer_segment_mask = ~customer_segments.isin(ALLOWED_CUSTOMER_SEGMENTS)

    valid_customers_df = customers_df[~invalid_customer_segment_mask].copy()
    invalid_customers_df = customers_df[invalid_customer_segment_mask].copy()

    return valid_customers_df, invalid_customers_df

def validate_customers(customers_df):
    validate_customers_schema(customers_df)

    # Run validations sequentially; only rows that pass continue to the next check
    valid_customers_df, invalid_id_df = validate_customer_ids(customers_df)

    valid_customers_df, invalid_name_df = validate_customer_names(valid_customers_df)

    valid_customers_df, invalid_city_df = validate_customer_cities(valid_customers_df)

    valid_customers_df, invalid_segment_df = validate_customer_segments(valid_customers_df)

    invalid_customers_df = pd.concat([invalid_id_df, invalid_name_df, invalid_city_df, invalid_segment_df], ignore_index=True)
    

    return valid_customers_df, invalid_customers_df

def validate_products_schema(products_df):
    expected_columns = ['product_id', 'product_name', 'category', 'brand', 'base_price', 'base_cost']
    actual_columns = products_df.columns.tolist()
    
    if actual_columns != expected_columns:
        raise ValueError(
            f"Product schema incorrect:\n"
            f"Expected: {expected_columns}\n"
            f"Received: {actual_columns}\n"
        )

def validate_product_ids(products_df):
    # Invalid IDs are missing, badly formatted, or duplicated after the first occurrence
    product_ids = products_df["product_id"].astype("string").str.strip()

    invalid_product_ids_mask = (
        product_ids.isna() |
        (product_ids == "") |
        ~product_ids.str.match(r"^P\d{4}$", na=False) |
        product_ids.duplicated()
    )

    valid_products_df = products_df[~invalid_product_ids_mask].copy()
    invalid_products_df = products_df[invalid_product_ids_mask].copy()

    return valid_products_df, invalid_products_df

def validate_product_names(products_df):
    product_names = products_df["product_name"].astype("string").str.strip()

    invalid_product_names_mask = (
        product_names.isna() |
        (product_names == "")
    )
    
    valid_products_df = products_df[~invalid_product_names_mask].copy()
    invalid_products_df = products_df[invalid_product_names_mask].copy()

    return valid_products_df, invalid_products_df

def validate_product_categories(products_df):
    product_categories = products_df["category"].astype("string").str.strip()

    invalid_product_categories_mask = ~product_categories.isin(ALLOWED_PRODUCT_CATEGORIES)

    valid_products_df = products_df[~invalid_product_categories_mask].copy()
    invalid_products_df = products_df[invalid_product_categories_mask].copy()

    return valid_products_df, invalid_products_df

def validate_product_brands(products_df):
    product_brands = products_df["brand"].astype("string").str.strip()

    invalid_product_brands_mask = (
        product_brands.isna() |
        (product_brands == "")
    )

    valid_products_df = products_df[~invalid_product_brands_mask].copy()
    invalid_products_df = products_df[invalid_product_brands_mask].copy()

    return valid_products_df, invalid_products_df

def validate_product_price_cost_values(products_df):
    # Reject non-numeric, zero, or negative price/cost values
    price = pd.to_numeric(products_df["base_price"], errors = "coerce")
    cost = pd.to_numeric(products_df["base_cost"], errors = "coerce")

    invalid_product_price_cost_values_mask = (
        price.isna() | cost.isna() |
        (price <= 0) | (cost <= 0)
    )
    
    valid_products_df = products_df[~invalid_product_price_cost_values_mask].copy()
    invalid_products_df = products_df[invalid_product_price_cost_values_mask].copy()

    return valid_products_df, invalid_products_df

def validate_product_price_cost_relationship(products_df):
    # Reject products where cost is greater than price
    price = pd.to_numeric(products_df["base_price"], errors = "coerce")
    cost = pd.to_numeric(products_df["base_cost"], errors = "coerce")

    invalid_product_price_cost_relationship_mask = (price < cost)

    valid_products_df = products_df[~invalid_product_price_cost_relationship_mask].copy()
    invalid_products_df = products_df[invalid_product_price_cost_relationship_mask].copy()

    return valid_products_df, invalid_products_df

def validate_products(products_df):
    validate_products_schema(products_df)

    # Run validations sequentially; only rows that pass continue to the next check
    valid_products_df, invalid_product_ids_df = validate_product_ids(products_df)
    valid_products_df, invalid_product_names_df = validate_product_names(valid_products_df)
    valid_products_df, invalid_products_categories_df = validate_product_categories(valid_products_df)
    valid_products_df, invalid_products_brands_df = validate_product_brands(valid_products_df)
    valid_products_df, invalid_product_price_cost_values = validate_product_price_cost_values(valid_products_df)
    valid_products_df, invalid_product_price_cost_relationship = validate_product_price_cost_relationship(valid_products_df)

    invalid_product_df =pd.concat(
        [
            invalid_product_ids_df, 
            invalid_product_names_df,
            invalid_products_categories_df,
            invalid_products_brands_df,
            invalid_product_price_cost_values,
            invalid_product_price_cost_relationship
        ] , ignore_index= True
    )
    
    return valid_products_df, invalid_product_df

def validate_stores_schema(stores_df):
    expected_columns = ["store_id", "store_name", "store_city"]
    actual_columns = stores_df.columns.tolist()

    if actual_columns != expected_columns:
        raise ValueError(
            f"Store schema incorrect\n"
            f"Expected: {expected_columns}\n"
            f"Received: {actual_columns}")

def validate_store_ids(stores_df):
    # Invalid IDs are missing, badly formatted, or duplicated after the first occurrence
    store_ids = stores_df["store_id"].astype("string").str.strip()

    invalid_store_ids_mask = (
        store_ids.isna() | 
        (store_ids== "") |
        ~store_ids.str.match(r"^ST\d{3}$", na=False) |
        store_ids.duplicated()
    )
    
    valid_stores_df= stores_df[~invalid_store_ids_mask].copy()
    invalid_stores_df= stores_df[invalid_store_ids_mask].copy()
    
    return valid_stores_df, invalid_stores_df

def validate_store_names(stores_df):
    store_names = stores_df["store_name"].astype("string").str.strip()

    invalid_store_names_mask = (
        store_names.isna() |
        (store_names=="")
    )

    valid_stores_df= stores_df[~invalid_store_names_mask].copy()
    invalid_stores_df= stores_df[invalid_store_names_mask].copy()

    return valid_stores_df, invalid_stores_df

def validate_store_cities(stores_df):
    store_cities = stores_df["store_city"].astype("string").str.strip()

    invalid_store_cities_mask = ~store_cities.isin(ALLOWED_STORE_CITIES)

    valid_stores_df = stores_df[~invalid_store_cities_mask].copy()
    invalid_stores_df = stores_df[invalid_store_cities_mask].copy()

    return valid_stores_df, invalid_stores_df

def validate_stores(stores_df):
    validate_stores_schema(stores_df)

    # Run validations sequentially; only rows that pass continue to the next check
    valid_stores_df, invalid_store_ids_df = validate_store_ids(stores_df)
    valid_stores_df, invalid_store_names_df = validate_store_names(valid_stores_df)
    valid_stores_df, invalid_store_cities_df = validate_store_cities(valid_stores_df)
    

    invalid_stores_df =pd.concat(
        [
            invalid_store_ids_df, 
            invalid_store_names_df,
            invalid_store_cities_df
        ] , ignore_index= True
    )
    
    return valid_stores_df, invalid_stores_df

def validate_sales_schema(sales_df):
    expected_columns = ['sale_id', 'customer_id', 'product_id', 'store_id', 'sale_date', 'quantity', 'unit_price', 'unit_cost']
    actual_columns = sales_df.columns.tolist()

    if actual_columns != expected_columns:
        raise ValueError(
            f"Sales schema incorrect\n"
            f"Expected: {expected_columns}\n"
            f"Received: {actual_columns}")

def validate_sale_ids(sales_df):
    sale_ids = sales_df["sale_id"].astype("string").str.strip()

    invalid_sale_ids_mask = (
        sale_ids.isna() |
        (sale_ids == "") |
        ~sale_ids.str.match(r"^S\d{6}$", na = False ) |
        sale_ids.duplicated()
    )

    valid_sales_df = sales_df[~invalid_sale_ids_mask].copy() 
    invalid_sales_df = sales_df[invalid_sale_ids_mask].copy()

    return valid_sales_df, invalid_sales_df

def validate_sale_customer_ids(sales_df, valid_customers_df):
    customer_ids = sales_df["customer_id"].astype("string").str.strip()
    valid_customer_ids = valid_customers_df["customer_id"].astype("string").str.strip()

    invalid_customer_ids_mask = (
        customer_ids.isna() |
        (customer_ids == "") |
        ~customer_ids.str.match(r"^C\d{4}$", na = False) |
        ~customer_ids.isin(valid_customer_ids)
    )

    valid_sales_df = sales_df[~invalid_customer_ids_mask].copy() 
    invalid_sales_df = sales_df[invalid_customer_ids_mask].copy()

    return valid_sales_df, invalid_sales_df    

def validate_sale_product_ids(sales_df, valid_products_df):
    product_ids = sales_df["product_id"].astype("string").str.strip()
    valid_product_ids = valid_products_df["product_id"].astype("string").str.strip()

    invalid_product_ids_mask = (
        product_ids.isna() |
        (product_ids == "") |
        ~product_ids.str.match(r"^P\d{4}$", na = False) |
        ~product_ids.isin(valid_product_ids)
    )
    
    valid_sales_df = sales_df[~invalid_product_ids_mask].copy() 
    invalid_sales_df = sales_df[invalid_product_ids_mask].copy()

    return valid_sales_df, invalid_sales_df 

def validate_sale_store_ids(sales_df, valid_stores_df):
    store_ids = sales_df["store_id"].astype("string").str.strip()
    valid_store_ids = valid_stores_df["store_id"].astype("string").str.strip()

    invalid_store_ids_mask = (
        store_ids.isna() |
        (store_ids == "") |
        ~store_ids.str.match(r"^ST\d{3}$", na = False) |
        ~store_ids.isin(valid_store_ids)
    )

    valid_sales_df = sales_df[~invalid_store_ids_mask].copy()
    invalid_sales_df = sales_df[invalid_store_ids_mask].copy()

    return valid_sales_df, invalid_sales_df

def validate_sale_dates(sales_df):
    sale_dates = pd.to_datetime(sales_df["sale_date"], errors="coerce", format="%Y-%m-%d")

    min_date = pd.Timestamp("2025-01-01")
    max_date = pd.Timestamp("2026-12-31")

    invalid_sale_dates_mask = (
        sale_dates.isna() |
        (sale_dates > max_date) |
        (sale_dates < min_date) 
    )

    valid_sales_df = sales_df[~invalid_sale_dates_mask].copy()
    invalid_sales_df = sales_df[invalid_sale_dates_mask].copy()

    return valid_sales_df, invalid_sales_df

def validate_sale_quantities(sales_df):
    quantities = pd.to_numeric(sales_df["quantity"], errors="coerce")

    invalid_sale_quantities_mask = (
        quantities.isna() |
        (quantities <= 0) |
        (quantities % 1 != 0)
    )

    valid_sales_df = sales_df[~invalid_sale_quantities_mask].copy()
    invalid_sales_df = sales_df[invalid_sale_quantities_mask].copy()

    return valid_sales_df, invalid_sales_df

def validate_sale_price_cost_values(sales_df):
    unit_prices = pd.to_numeric(sales_df["unit_price"], errors= "coerce")
    unit_costs = pd.to_numeric(sales_df["unit_cost"], errors= "coerce")

    invalid_price_cost_values_mask = (
        unit_prices.isna() | unit_costs.isna() |
        (unit_prices <= 0) | (unit_costs <= 0)
    )

    valid_sales_df = sales_df[~invalid_price_cost_values_mask].copy()
    invalid_sales_df = sales_df[invalid_price_cost_values_mask].copy()

    return valid_sales_df, invalid_sales_df

def validate_sale_price_cost_relationship(sales_df):
    unit_prices = pd.to_numeric(sales_df["unit_price"], errors= "coerce")
    unit_costs = pd.to_numeric(sales_df["unit_cost"], errors= "coerce")
    
    invalid_sale_price_cost_relationship_mask = unit_costs > unit_prices

    valid_sales_df = sales_df[~invalid_sale_price_cost_relationship_mask].copy()
    invalid_sales_df = sales_df[invalid_sale_price_cost_relationship_mask].copy()

    return valid_sales_df, invalid_sales_df

def validate_sales(sales_df, valid_customers_df, valid_products_df, valid_stores_df):
    validate_sales_schema(sales_df)

    # Run validations sequentially; only rows that pass continue to the next check
    valid_sales_df, invalid_sale_ids_df = validate_sale_ids(sales_df)

    valid_sales_df, invalid_customer_ids_df = validate_sale_customer_ids(
        valid_sales_df,
        valid_customers_df
    )

    valid_sales_df, invalid_product_ids_df = validate_sale_product_ids(
        valid_sales_df,
        valid_products_df
    )

    valid_sales_df, invalid_store_ids_df = validate_sale_store_ids(
        valid_sales_df,
        valid_stores_df
    )

    valid_sales_df, invalid_sale_dates_df = validate_sale_dates(valid_sales_df)

    valid_sales_df, invalid_quantities_df = validate_sale_quantities(valid_sales_df)

    valid_sales_df, invalid_price_cost_values_df = validate_sale_price_cost_values(valid_sales_df)

    valid_sales_df, invalid_price_cost_relationship_df = validate_sale_price_cost_relationship(valid_sales_df)

    invalid_sales_df = pd.concat(
        [
            invalid_sale_ids_df,
            invalid_customer_ids_df,
            invalid_product_ids_df,
            invalid_store_ids_df,
            invalid_sale_dates_df,
            invalid_quantities_df,
            invalid_price_cost_values_df,
            invalid_price_cost_relationship_df,
        ],
        ignore_index=True
    )

    return valid_sales_df, invalid_sales_df

def validate_all(customers_df, products_df, stores_df, sales_df):
    valid_customers_df, invalid_customers_df = validate_customers(customers_df)
    valid_products_df, invalid_products_df = validate_products(products_df)
    valid_stores_df, invalid_stores_df = validate_stores(stores_df)

    valid_sales_df, invalid_sales_df = validate_sales(
        sales_df,
        valid_customers_df,
        valid_products_df,
        valid_stores_df
    )

    valid_data = {
        "customers": valid_customers_df,
        "products": valid_products_df,
        "stores": valid_stores_df,
        "sales": valid_sales_df,
    }

    invalid_data = {
        "customers": invalid_customers_df,
        "products": invalid_products_df,
        "stores": invalid_stores_df,
        "sales": invalid_sales_df,
    }

    return valid_data, invalid_data

if __name__ == "__main__":
    data = extract_all()

    valid_data, invalid_data = validate_all(
        data["customers"],
        data["products"],
        data["stores"],
        data["sales"]
    )

    print("Validation summary:")
    print("-------------------")

    for table_name in valid_data:
        print(f"{table_name.capitalize()}:")
        print(f"  Valid rows: {len(valid_data[table_name])}")
        print(f"  Invalid rows: {len(invalid_data[table_name])}")

    print("\nInvalid sales preview:")
    if not invalid_data["sales"].empty:
        print(invalid_data["sales"])
    else:
        print("No invalid sales found.")