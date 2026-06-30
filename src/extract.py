import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

def get_data_path(filename):
    return DATA_DIR / filename

def extract_customers():
    path = get_data_path("customers.csv")
    return pd.read_csv(path)

def extract_products():
    path = get_data_path("products.csv")
    return pd.read_csv(path)

def extract_stores():
    path = get_data_path("stores.csv")
    return pd.read_csv(path)

def extract_sales():
    path = get_data_path("sales.csv")
    return pd.read_csv(path)

def extract_all():
    customers_df = extract_customers()
    products_df = extract_products()
    stores_df = extract_stores()
    sales_df = extract_sales()

    data = {
        "customers": customers_df,
        "products": products_df,
        "stores": stores_df,
        "sales": sales_df,
    }

    return data