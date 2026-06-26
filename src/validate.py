from extract import extract_all
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

    invalid_customer_id_mask = (
        customer_ids.isna() | 
        (customer_ids== "") |
        ~customer_ids.str.match(r"^C\d{4}$", na=False) |
        customer_ids.duplicated()
    )
    
    valid_customers_df= customers_df[~invalid_customer_id_mask].copy()
    invalid_customers_df= customers_df[invalid_customer_id_mask].copy()
    
    return valid_customers_df, invalid_customers_df

def validate_customer_name(customers_df):
    customer_names = customers_df["customer_name"].astype("string").str.strip()

    invalid_customer_name_mask = (
        customer_names.isna() |
        (customer_names=="")
    )

    valid_customers_df= customers_df[~invalid_customer_name_mask].copy()
    invalid_customers_df= customers_df[invalid_customer_name_mask].copy()

    return valid_customers_df, invalid_customers_df

def validate_customer_city(customers_df):
    customer_cities = customers_df["customer_city"].astype("string").str.strip()
    invalid_customer_city_mask = ~customer_cities.isin(ALLOWED_CITIES)
    
    valid_customers_df = customers_df[~invalid_customer_city_mask].copy()
    invalid_customers_df = customers_df[invalid_customer_city_mask].copy()

    return valid_customers_df, invalid_customers_df

def validate_customer_segment(customers_df):
    customer_segments = customers_df["customer_segment"].astype("string").str.strip()
    invalid_customer_segment_mask = ~customer_segments.isin(ALLOWED_CUSTOMER_SEGMENTS)

    valid_customers_df = customers_df[~invalid_customer_segment_mask].copy()
    invalid_customers_df = customers_df[invalid_customer_segment_mask].copy()

    return valid_customers_df, invalid_customers_df

def validate_customers(customers_df):
    validate_customers_schema(customers_df)

    # Run validations sequentially; only rows that pass continue to the next check
    valid_customers_df, invalid_id_df = validate_customer_ids(customers_df)

    valid_customers_df, invalid_name_df = validate_customer_name(valid_customers_df)

    valid_customers_df, invalid_city_df = validate_customer_city(valid_customers_df)

    valid_customers_df, invalid_segment_df = validate_customer_segment(valid_customers_df)

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



#valide products
#validate stores
#valide sales
#validate all


if __name__ == "__main__":
    data = extract_all()
    validate_products_schema(data["products"])
    valid_products_df, invalid_products_df = validate_products(data["products"])

    print(f"Valid customers: {len(valid_products_df)}")
    print(f"Invalid customers: {len(invalid_products_df)}")

    if not invalid_products_df.empty:
        print(invalid_products_df)

   