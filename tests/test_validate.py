import pytest
import pandas as pd
from src.validate import (validate_customers_schema, validate_customer_ids, validate_customer_names, validate_customer_cities, validate_customer_segments)

@pytest.fixture
def valid_customer_data():
    data = {
        "customer_id" : "C0134",
        "customer_name" : "Ahmad Ali",
        "customer_city" : "Amman",
        "customer_segment" : "Premium",
     }
    
    return pd.DataFrame([data])

def test_validate_customer_schema_rejects_incorrect_schema(valid_customer_data):
    valid_data = valid_customer_data.copy()

    invalid_data = valid_data.drop(columns=["customer_name"])

    with pytest.raises(ValueError):
        validate_customers_schema(invalid_data)

def test_validate_customer_ids_rejects_bad_format(valid_customer_data):
    bad_customer = valid_customer_data.copy()

    bad_customer.loc[0, "customer_id"] = "Bad_id"

    valid_df, invalid_df = validate_customer_ids(bad_customer)

    assert len(valid_df) == 0
    assert len(invalid_df) == 1
    assert invalid_df.iloc[0]["customer_id"] == "Bad_id"

def test_validate_customer_names_rejects_empty_name(valid_customer_data):
    bad_customer = valid_customer_data.copy()

    bad_customer.loc[0, "customer_name"] = ""

    valid_df, invalid_df = validate_customer_names(bad_customer)

    assert len(valid_df) == 0
    assert len(invalid_df) == 1
    assert invalid_df.iloc[0]["customer_name"] == ""

def test_validate_customer_cities_rejects_incorrect_city(valid_customer_data):
    bad_customer = valid_customer_data.copy()

    bad_customer.loc[0, "customer_city"] = "Cairo"

    valid_df, invalid_df = validate_customer_cities(bad_customer)

    assert len(valid_df) == 0
    assert len(invalid_df) == 1
    assert invalid_df.iloc[0]["customer_city"] == "Cairo"

def test_validate_customer_segments_rejects_incorrect_segment(valid_customer_data):
    bad_customer = valid_customer_data.copy()

    bad_customer.loc[0, "customer_segment"] = "Extra"

    valid_df, invalid_df = validate_customer_segments(bad_customer)

    assert len(valid_df) == 0
    assert len(invalid_df) == 1
    assert invalid_df.iloc[0]["customer_segment"] == "Extra"

