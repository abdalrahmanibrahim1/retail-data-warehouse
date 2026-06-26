from extract import extract_all
import pandas as pd

#constants, allowed values
ALLOWED_CITIES = {"Amman", "Irbid", "Zarqa", "Aqaba", "Salt", "Madaba", "Jerash"}
ALLOWED_CUSTOMER_SEGMENTS = {"Regular", "Premium", "Student", "Business"}

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

#validate customers
#valide products
#validate stores
#valide sales
#validate all


if __name__ == "__main__":
    data = extract_all()

    valid_customers_df, invalid_customers_df = validate_customers(data["customers"])

    print(f"Valid customers: {len(valid_customers_df)}")
    print(f"Invalid customers: {len(invalid_customers_df)}")

    if not invalid_customers_df.empty:
        print(invalid_customers_df)

   