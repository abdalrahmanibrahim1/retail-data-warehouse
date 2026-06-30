"""
Tests for the transformation layer.

These tests verify that validated source data is transformed into the expected
warehouse dimension and fact tables, including surrogate keys, date keys, and
fact measures.
"""

import pytest
import pandas as pd
import src.transform as transform

@pytest.fixture
def valid_customer():
    customer = {
        "customer_id": "C0001",
        "customer_name": "Ahmad Ali",
        "customer_city": "Amman",
        "customer_segment": "Premium",
    }

    return customer

@pytest.fixture
def valid_product():
    product = {
        "product_id": "P0001",
        "product_name": "Blow dryer",
        "category": "Electronics",
        "brand": "Anker",
        "base_price": 16.8,
        "base_cost": 10.0,
    }    

    return product

@pytest.fixture
def valid_store():
    store = {
        "store_id": "ST001",
        "store_name": "Downtown Amman Store",
        "store_city": "Amman",
    }

    return store

@pytest.fixture
def valid_sale():
    sale = {
        "sale_id" : "S000001",
        "customer_id" : "C0001",
        "product_id" : "P0001",
        "store_id" : "ST001",
        "sale_date" : "2025-06-15",
        "quantity" : 2,
        "unit_price" : 20,
        "unit_cost" : 12,
    }

    return pd.DataFrame([sale])

def test_build_dim_customers_adds_customer_key(valid_customer):
    customer_df = pd.DataFrame([valid_customer])
    dim_customer = transform.build_dim_customer(customer_df)

    assert "customer_key" in dim_customer.columns
    assert dim_customer.iloc[0]["customer_key"] == 1
    assert len(dim_customer) == 1

def test_build_dim_products_adds_product_key(valid_product):
    product_df = pd.DataFrame([valid_product])
    dim_product = transform.build_dim_product(product_df)

    assert "product_key" in dim_product.columns
    assert "base_price" not in dim_product.columns
    assert "base_cost" not in dim_product.columns
    assert dim_product.iloc[0]["product_id"] == "P0001"
    assert dim_product.iloc[0]["product_key"] == 1
    assert len(dim_product) == 1

def test_build_dim_stores_adds_store_key(valid_store):
    stores_df = pd.DataFrame([valid_store])
    dim_store = transform.build_dim_store(stores_df)

    assert "store_key" in dim_store.columns
    assert dim_store.iloc[0]["store_key"] == 1
    assert dim_store.iloc[0]["store_id"] == "ST001"
    assert len(dim_store) == 1

def test_build_dim_date_creates_expected_date_dimension():
    dim_date = transform.build_dim_date()

    assert len(dim_date) == 730
    assert list(dim_date.columns) == [
        "date_key",
        "full_date",
        "year",
        "quarter",
        "month",
        "day",
        "weekday",
    ]

    first_row = dim_date.iloc[0]

    assert first_row["date_key"] == 20250101
    assert first_row["year"] == 2025
    assert first_row["quarter"] == 1
    assert first_row["month"] == 1
    assert first_row["day"] == 1
    assert first_row["weekday"] == "Wednesday"

    last_row = dim_date.iloc[-1]

    assert last_row["date_key"] == 20261231
    assert last_row["year"] == 2026
    assert last_row["month"] == 12
    assert last_row["day"] == 31


def test_build_fact_sales_maps_keys_and_calculates_measures(valid_customer, valid_product, valid_store, valid_sale):
    dim_customer = transform.build_dim_customer(pd.DataFrame([valid_customer]))
    dim_product = transform.build_dim_product(pd.DataFrame([valid_product]))
    dim_store = transform.build_dim_store(pd.DataFrame([valid_store]))
    dim_date = transform.build_dim_date()

    fact_sales = transform.build_fact_sales(valid_sale, dim_customer, dim_product, dim_store, dim_date)

    assert list(fact_sales.columns) == [
        "sale_key",
        "sale_id",
        "customer_key",
        "product_key",
        "store_key",
        "date_key",
        "quantity",
        "revenue",
        "profit",
    ]

    row = fact_sales.iloc[0]

    assert row["sale_key"] == 1
    assert row["sale_id"] == "S000001"
    assert row["customer_key"] == 1
    assert row["product_key"] == 1
    assert row["store_key"] == 1
    assert row["date_key"] == 20250615
    assert row["quantity"] == 2
    assert row["revenue"] == 40
    assert row["profit"] == 16

def test_transform_all_returns_all_warehouse_tables(
    valid_customer,
    valid_product,
    valid_store,
    valid_sale
):
    valid_data = {
        "customers": pd.DataFrame([valid_customer]),
        "products": pd.DataFrame([valid_product]),
        "stores": pd.DataFrame([valid_store]),
        "sales": valid_sale,
    }

    transformed_data = transform.transform_all(valid_data)

    assert len(transformed_data) == 5

    assert "dim_customer" in transformed_data
    assert "dim_product" in transformed_data
    assert "dim_store" in transformed_data
    assert "dim_date" in transformed_data
    assert "fact_sales" in transformed_data

    assert len(transformed_data["dim_customer"]) == 1
    assert len(transformed_data["dim_product"]) == 1
    assert len(transformed_data["dim_store"]) == 1
    assert len(transformed_data["dim_date"]) == 730
    assert len(transformed_data["fact_sales"]) == 1