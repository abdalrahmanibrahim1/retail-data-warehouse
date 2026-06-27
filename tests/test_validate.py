import pytest
import pandas as pd
import src.validate as validate
@pytest.fixture
def valid_customer_data():
    data = {
        "customer_id" : "C0134",
        "customer_name" : "Ahmad Ali",
        "customer_city" : "Amman",
        "customer_segment" : "Premium",
     }
    
    return pd.DataFrame([data])

@pytest.fixture
def valid_product_data():
    data = {
        "product_id" : "P0100",
        "product_name" : "Blow dryer",
        "category" : "Electronics",
        "brand" : "Anker",
        "base_price" : 16.8,
        "base_cost": 10.0,
     }
    
    return pd.DataFrame([data])

@pytest.fixture
def valid_store_data():
    data = {
        "store_id": "ST001",
        "store_name": "Amman Main Store",
        "store_city": "Amman",
    }

    return pd.DataFrame([data])


def test_validate_customer_schema_rejects_incorrect_schema(valid_customer_data):
    valid_data = valid_customer_data.copy()

    invalid_data = valid_data.drop(columns=["customer_name"])

    with pytest.raises(ValueError):
        validate.validate_customers_schema(invalid_data)

def test_validate_customer_ids_rejects_bad_format(valid_customer_data):
    bad_customer = valid_customer_data.copy()

    bad_customer.loc[0, "customer_id"] = "Bad_id"

    valid_df, invalid_df = validate.validate_customer_ids(bad_customer)

    assert len(valid_df) == 0
    assert len(invalid_df) == 1
    assert invalid_df.iloc[0]["customer_id"] == "Bad_id"

def test_validate_customer_names_rejects_empty_name(valid_customer_data):
    bad_customer = valid_customer_data.copy()

    bad_customer.loc[0, "customer_name"] = ""

    valid_df, invalid_df = validate.validate_customer_names(bad_customer)

    assert len(valid_df) == 0
    assert len(invalid_df) == 1
    assert invalid_df.iloc[0]["customer_name"] == ""

def test_validate_customer_cities_rejects_incorrect_city(valid_customer_data):
    bad_customer = valid_customer_data.copy()

    bad_customer.loc[0, "customer_city"] = "Cairo"

    valid_df, invalid_df = validate.validate_customer_cities(bad_customer)

    assert len(valid_df) == 0
    assert len(invalid_df) == 1
    assert invalid_df.iloc[0]["customer_city"] == "Cairo"

def test_validate_customer_segments_rejects_incorrect_segment(valid_customer_data):
    bad_customer = valid_customer_data.copy()

    bad_customer.loc[0, "customer_segment"] = "Extra"

    valid_df, invalid_df = validate.validate_customer_segments(bad_customer)

    assert len(valid_df) == 0
    assert len(invalid_df) == 1
    assert invalid_df.iloc[0]["customer_segment"] == "Extra"

def test_validate_product_schema_rejects_incorrect_schema(valid_product_data):
    bad_data = valid_product_data.copy()
    bad_data = bad_data.drop(columns=["product_id"])

    with pytest.raises(ValueError):
        validate.validate_products_schema(bad_data)

def test_validate_product_names_rejects_missing_name(valid_product_data):
    bad_data = valid_product_data.copy()
    bad_data.loc[0,"product_name"] = None

    valid_df, invalid_df = validate.validate_product_names(bad_data)

    assert len(valid_df) == 0
    assert len(invalid_df) == 1
    assert pd.isna(invalid_df.iloc[0]["product_name"])

def test_validate_product_categories_rejects_invalid_category(valid_product_data):
    bad_data = valid_product_data.copy()
    bad_data.loc[0, "category"] = "Jordan"

    valid_df, invalid_df = validate.validate_product_categories(bad_data)

    assert len(valid_df) == 0
    assert len(invalid_df) == 1
    assert invalid_df.iloc[0]["category"] == "Jordan"

def test_validate_product_brands_rejects_missing_brand(valid_product_data):
    bad_data = valid_product_data.copy()
    bad_data.loc[0, "brand"] = None

    valid_df, invalid_df = validate.validate_product_brands(bad_data)

    assert len(valid_df) == 0
    assert len(invalid_df) == 1
    assert pd.isna(invalid_df.iloc[0]["brand"])

def test_validate_product_price_cost_values_rejects_non_positive_values(valid_product_data):
    bad_data = valid_product_data.copy()
    bad_data.loc[0, "base_price"] = 0

    valid_df, invalid_df = validate.validate_product_price_cost_values(bad_data)

    assert len(valid_df) == 0
    assert len(invalid_df) == 1
    assert invalid_df.iloc[0]["base_price"] == 0

def test_validate_product_price_cost_relationship_rejects_invalid_relationship(valid_product_data):
    bad_data = valid_product_data.copy()
    bad_data.loc[0, "base_price"] = 3
    bad_data.loc[0, "base_cost"] = 20

    valid_df, invalid_df = validate.validate_product_price_cost_relationship(bad_data)

    assert len(valid_df) == 0
    assert len(invalid_df) == 1
    assert (invalid_df.iloc[0]["base_price"] - invalid_df.iloc[0]["base_cost"]) < 0

def test_validate_store_schema_rejects_incorrect_schema(valid_store_data):
    bad_data = valid_store_data.copy()
    bad_data = bad_data.drop(columns = ["store_name"])

    with pytest.raises(ValueError):
        validate.validate_stores_schema(bad_data)
    
def test_validate_store_ids_rejects_missing_id(valid_store_data):
    bad_data = valid_store_data.copy()
    bad_data.loc[0,"store_id"] = None

    valid_df, invalid_df = validate.validate_store_ids(bad_data)

    assert len(valid_df) == 0
    assert len(invalid_df) == 1
    assert pd.isna(invalid_df.iloc[0]["store_id"])

def test_validate_store_names_rejects_empty_name(valid_store_data):
    bad_data = valid_store_data.copy()
    bad_data.loc[0,"store_name"] = ""

    valid_df, invalid_df = validate.validate_store_names(bad_data)

    assert len(valid_df) == 0
    assert len(invalid_df) == 1
    assert invalid_df.iloc[0]["store_name"] == ""

def test_validate_store_cities_rejects_invalid_city(valid_store_data):
    bad_data = valid_store_data.copy()
    bad_data.loc[0, "store_city"] = "Miami"

    valid_df, invalid_df = validate.validate_store_cities(bad_data)

    assert len(valid_df) == 0
    assert len(invalid_df) == 1
    assert invalid_df.iloc[0]["store_city"] == "Miami"
