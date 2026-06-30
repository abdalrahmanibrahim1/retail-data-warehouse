import pandas as pd

#constants, allowed values
ALLOWED_CITIES = {"Amman", "Irbid", "Zarqa", "Aqaba", "Salt", "Madaba", "Jerash"}
ALLOWED_CUSTOMER_SEGMENTS = {"Regular", "Premium", "Student", "Business"}
ALLOWED_PRODUCT_CATEGORIES = {"Electronics", "Clothing", "Footwear", "Grocery", "Home", "Beauty", "Sports", "Books"}
ALLOWED_STORE_CITIES = {"Amman", "Irbid", "Zarqa", "Aqaba", "Salt", "Madaba", "Jerash"}

def validate_customers_schema(customers_df):
    """
    Verify that the customers source table has exactly the expected columns.

    Column order is checked intentionally so the pipeline fails fast if the source
    CSV structure changes unexpectedly.
    """
    expected_columns = ['customer_id', 'customer_name', 'customer_city', 'customer_segment']
    actual_columns = customers_df.columns.tolist()

    if actual_columns != expected_columns:
        raise ValueError(
            f"Customer schema incorrect\n"
            f"Expected: {expected_columns}\n"
            f"Received: {actual_columns}")

def validate_customer_ids(customers_df):
    """
    Split customer rows based on customer_id validity.

    A valid customer_id must be non-empty, unique, and match the format C0001.
    Duplicate IDs are rejected after the first occurrence.
    """
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
    """
    Split customer rows based on whether customer_name is present.
    """
    customer_names = customers_df["customer_name"].astype("string").str.strip()

    invalid_customer_names_mask = (
        customer_names.isna() |
        (customer_names=="")
    )

    valid_customers_df= customers_df[~invalid_customer_names_mask].copy()
    invalid_customers_df= customers_df[invalid_customer_names_mask].copy()

    return valid_customers_df, invalid_customers_df

def validate_customer_cities(customers_df):
    """
    Split customer rows based on whether customer_city is in the allowed city list.
    """
    customer_cities = customers_df["customer_city"].astype("string").str.strip()
    invalid_customer_city_mask = ~customer_cities.isin(ALLOWED_CITIES)
    
    valid_customers_df = customers_df[~invalid_customer_city_mask].copy()
    invalid_customers_df = customers_df[invalid_customer_city_mask].copy()

    return valid_customers_df, invalid_customers_df

def validate_customer_segments(customers_df):
    """
    Split customer rows based on whether customer_segment is in the allowed segment list.
    """
    customer_segments = customers_df["customer_segment"].astype("string").str.strip()
    invalid_customer_segment_mask = ~customer_segments.isin(ALLOWED_CUSTOMER_SEGMENTS)

    valid_customers_df = customers_df[~invalid_customer_segment_mask].copy()
    invalid_customers_df = customers_df[invalid_customer_segment_mask].copy()

    return valid_customers_df, invalid_customers_df

def validate_customers(customers_df):
    """
    Validate the customers source table and return separate valid and invalid rows.

    Validation runs sequentially. Rows that fail one rule are removed from the valid
    set before the next rule is checked, which prevents the same row from being
    counted as invalid multiple times.
    """
    validate_customers_schema(customers_df)

    valid_customers_df, invalid_id_df = validate_customer_ids(customers_df)

    valid_customers_df, invalid_name_df = validate_customer_names(valid_customers_df)

    valid_customers_df, invalid_city_df = validate_customer_cities(valid_customers_df)

    valid_customers_df, invalid_segment_df = validate_customer_segments(valid_customers_df)

    invalid_customers_df = pd.concat(
        [invalid_id_df, invalid_name_df, invalid_city_df, invalid_segment_df],
        ignore_index=True
    )
    

    return valid_customers_df, invalid_customers_df

def validate_products_schema(products_df):
    """
    Verify that the products source table has exactly the expected columns.

    Column order is checked intentionally so the pipeline fails fast if the source
    CSV structure changes unexpectedly.
    """
    expected_columns = ['product_id', 'product_name', 'category', 'brand', 'base_price', 'base_cost']
    actual_columns = products_df.columns.tolist()
    
    if actual_columns != expected_columns:
        raise ValueError(
            f"Product schema incorrect:\n"
            f"Expected: {expected_columns}\n"
            f"Received: {actual_columns}\n"
        )

def validate_product_ids(products_df):
    """
    Split product rows based on product_id validity.

    A valid product_id must be non-empty, unique, and match the format P0001.
    Duplicate IDs are rejected after the first occurrence.
    """
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
    """
    Split product rows based on whether product_name is present.
    """
    product_names = products_df["product_name"].astype("string").str.strip()

    invalid_product_names_mask = (
        product_names.isna() |
        (product_names == "")
    )
    
    valid_products_df = products_df[~invalid_product_names_mask].copy()
    invalid_products_df = products_df[invalid_product_names_mask].copy()

    return valid_products_df, invalid_products_df

def validate_product_categories(products_df):
    """
    Split product rows based on whether category is in the allowed product category list.
    """
    product_categories = products_df["category"].astype("string").str.strip()

    invalid_product_categories_mask = ~product_categories.isin(ALLOWED_PRODUCT_CATEGORIES)

    valid_products_df = products_df[~invalid_product_categories_mask].copy()
    invalid_products_df = products_df[invalid_product_categories_mask].copy()

    return valid_products_df, invalid_products_df

def validate_product_brands(products_df):
    """
    Split product rows based on whether brand is present.
    """
    product_brands = products_df["brand"].astype("string").str.strip()

    invalid_product_brands_mask = (
        product_brands.isna() |
        (product_brands == "")
    )

    valid_products_df = products_df[~invalid_product_brands_mask].copy()
    invalid_products_df = products_df[invalid_product_brands_mask].copy()

    return valid_products_df, invalid_products_df

def validate_product_price_cost_values(products_df):
    """
    Split product rows based on whether base_price and base_cost are valid positive numbers.
    """
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
    """
    Split product rows based on whether base_cost is less than or equal to base_price.

    Equality is allowed, but cost greater than price is rejected because it would
    create negative product-level margin.
    """
    price = pd.to_numeric(products_df["base_price"], errors = "coerce")
    cost = pd.to_numeric(products_df["base_cost"], errors = "coerce")

    invalid_product_price_cost_relationship_mask = (price < cost)

    valid_products_df = products_df[~invalid_product_price_cost_relationship_mask].copy()
    invalid_products_df = products_df[invalid_product_price_cost_relationship_mask].copy()

    return valid_products_df, invalid_products_df

def validate_products(products_df):
    """
    Validate the products source table and return separate valid and invalid rows.

    Validation runs sequentially. Rows that fail one rule are removed from the valid
    set before the next rule is checked, which prevents the same row from being
    counted as invalid multiple times.
    """
    validate_products_schema(products_df)

    valid_products_df, invalid_product_ids_df = validate_product_ids(products_df)

    valid_products_df, invalid_product_names_df = validate_product_names(valid_products_df)

    valid_products_df, invalid_products_categories_df = validate_product_categories(valid_products_df)

    valid_products_df, invalid_products_brands_df = validate_product_brands(valid_products_df)

    valid_products_df, invalid_product_price_cost_values_df = validate_product_price_cost_values(valid_products_df)

    valid_products_df, invalid_product_price_cost_relationship_df = validate_product_price_cost_relationship(valid_products_df)

    invalid_products_df =pd.concat(
        [
            invalid_product_ids_df, 
            invalid_product_names_df,
            invalid_products_categories_df,
            invalid_products_brands_df,
            invalid_product_price_cost_values_df,
            invalid_product_price_cost_relationship_df
        ] , ignore_index= True
    )
    
    return valid_products_df, invalid_products_df

def validate_stores_schema(stores_df):
    """
    Verify that the stores source table has exactly the expected columns.

    Column order is checked intentionally so the pipeline fails fast if the source
    CSV structure changes unexpectedly.
    """
    expected_columns = ["store_id", "store_name", "store_city"]
    actual_columns = stores_df.columns.tolist()

    if actual_columns != expected_columns:
        raise ValueError(
            f"Store schema incorrect\n"
            f"Expected: {expected_columns}\n"
            f"Received: {actual_columns}")

def validate_store_ids(stores_df):
    """
    Split store rows based on store_id validity.

    A valid store_id must be non-empty, unique, and match the format ST001.
    Duplicate IDs are rejected after the first occurrence.
    """
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
    """
    Split store rows based on whether store_name is present.
    """
    store_names = stores_df["store_name"].astype("string").str.strip()

    invalid_store_names_mask = (
        store_names.isna() |
        (store_names=="")
    )

    valid_stores_df= stores_df[~invalid_store_names_mask].copy()
    invalid_stores_df= stores_df[invalid_store_names_mask].copy()

    return valid_stores_df, invalid_stores_df

def validate_store_cities(stores_df):
    """
    Split store rows based on whether store_city is in the allowed store city list.
    """
    store_cities = stores_df["store_city"].astype("string").str.strip()

    invalid_store_cities_mask = ~store_cities.isin(ALLOWED_STORE_CITIES)

    valid_stores_df = stores_df[~invalid_store_cities_mask].copy()
    invalid_stores_df = stores_df[invalid_store_cities_mask].copy()

    return valid_stores_df, invalid_stores_df

def validate_stores(stores_df):
    """
    Validate the stores source table and return separate valid and invalid rows.

    Validation runs sequentially. Rows that fail one rule are removed from the valid
    set before the next rule is checked, which prevents the same row from being
    counted as invalid multiple times.
    """
    validate_stores_schema(stores_df)

    # Run validations sequentially; only rows that pass continue to the next check
    valid_stores_df, invalid_store_ids_df = validate_store_ids(stores_df)

    valid_stores_df, invalid_store_names_df = validate_store_names(valid_stores_df)

    valid_stores_df, invalid_store_cities_df = validate_store_cities(valid_stores_df)
    

    invalid_stores_df = pd.concat(
        [
            invalid_store_ids_df, 
            invalid_store_names_df,
            invalid_store_cities_df
        ], 
        ignore_index= True
    )
    
    return valid_stores_df, invalid_stores_df

def validate_sales_schema(sales_df):
    """
    Verify that the sales source table has exactly the expected columns.

    Column order is checked intentionally so the pipeline fails fast if the source
    CSV structure changes unexpectedly.
    """
    expected_columns = ['sale_id', 'customer_id', 'product_id', 'store_id', 'sale_date', 'quantity', 'unit_price', 'unit_cost']
    actual_columns = sales_df.columns.tolist()

    if actual_columns != expected_columns:
        raise ValueError(
            f"Sales schema incorrect\n"
            f"Expected: {expected_columns}\n"
            f"Received: {actual_columns}")

def validate_sale_ids(sales_df):
    """
    Split sales rows based on sale_id validity.

    A valid sale_id must be non-empty, unique, and match the format S000001.
    Duplicate IDs are rejected after the first occurrence.
    """
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
    """
    Split sales rows based on whether customer_id is valid and references a valid customer.

    Sales are checked against the already-validated customers table so rejected
    customer rows cannot appear as valid references in the fact table.
    """
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
    """
    Split sales rows based on whether product_id is valid and references a valid product.

    Sales are checked against the already-validated products table so rejected
    product rows cannot appear as valid references in the fact table.
    """
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
    """
    Split sales rows based on whether store_id is valid and references a valid store.

    Sales are checked against the already-validated stores table so rejected
    store rows cannot appear as valid references in the fact table.
    """
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
    """
    Split sales rows based on whether sale_date is a valid date within the warehouse date range.

    The project date dimension covers 2025-01-01 through 2026-12-31, so sales
    outside that range are rejected.
    """
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
    """
    Split sales rows based on whether quantity is a positive whole number.
    """
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
    """
    Split sales rows based on whether unit_price and unit_cost are valid positive numbers.
    """
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
    """
    Split sales rows based on whether unit_cost is less than or equal to unit_price.

    Equality is allowed, but unit_cost greater than unit_price is rejected because
    it would create negative profit in the fact table.
    """
    unit_prices = pd.to_numeric(sales_df["unit_price"], errors= "coerce")
    unit_costs = pd.to_numeric(sales_df["unit_cost"], errors= "coerce")
    
    invalid_sale_price_cost_relationship_mask = unit_costs > unit_prices

    valid_sales_df = sales_df[~invalid_sale_price_cost_relationship_mask].copy()
    invalid_sales_df = sales_df[invalid_sale_price_cost_relationship_mask].copy()

    return valid_sales_df, invalid_sales_df

def validate_sales(sales_df, valid_customers_df, valid_products_df, valid_stores_df):
    """
    Validate the sales source table and return separate valid and invalid rows.

    Sales validation runs after customer, product, and store validation because
    each sale must reference valid dimension records. Validation is sequential:
    rows that fail one rule are removed before the next rule runs, preventing the
    same row from being counted as invalid multiple times.
    """
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

def validate_all(data):
    """
    Validate all extracted source tables and return valid and invalid datasets.

    The input is the dictionary returned by extract_all(), with one DataFrame for
    each source table. Customer, product, and store tables are validated first.
    Sales are validated last because each sale must reference dimension records
    that already passed validation.
    """
    valid_customers_df, invalid_customers_df = validate_customers(data["customers"])
    valid_products_df, invalid_products_df = validate_products(data["products"])
    valid_stores_df, invalid_stores_df = validate_stores(data["stores"])

    valid_sales_df, invalid_sales_df = validate_sales(
        data["sales"],
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