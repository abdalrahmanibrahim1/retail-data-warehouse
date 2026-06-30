"""
Integration tests for the loaded PostgreSQL warehouse.

These tests assume the pipeline has already loaded the warehouse and verify that
the final database tables exist, contain data, preserve foreign-key integrity,
and contain valid fact measures.
"""
import src.load as load
import pytest

@pytest.fixture
def db_cursor():
    """
    Open a database cursor for each test and close it after the test finishes.
    """
    conn = load.get_connection()
    cursor = conn.cursor()

    yield cursor

    cursor.close()
    conn.close()


def test_all_five_tables_exist(db_cursor):
    db_cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """
    )

    result = db_cursor.fetchall()
    
    tables = [item for tup in result for item in tup]

    assert 'dim_customer' in tables
    assert 'dim_product' in tables
    assert 'dim_store' in tables
    assert 'dim_date' in tables
    assert 'fact_sales' in tables

def test_warehouse_tables_are_not_empty(db_cursor):
    expected_counts = {
        "dim_customer": "not_empty",
        "dim_product": "not_empty",
        "dim_store": "not_empty",
        "dim_date": 730,
        "fact_sales": "not_empty",
    }

    for table, expectation in expected_counts.items():
        db_cursor.execute(f"SELECT COUNT(*) FROM {table};")
        row_count, = db_cursor.fetchone()

        if expectation == "not_empty":
            assert row_count > 0
        else:
            assert row_count == expectation

def test_fact_sales_has_no_orphan_foreign_keys(db_cursor):
    # Each fact foreign key must match an existing dimension key.
    relationships = {
        "dim_customer": "customer_key",
        "dim_product" : "product_key",
        "dim_store" : "store_key",
        "dim_date" : "date_key"
    }

    for dim, key in relationships.items():
        db_cursor.execute(
        f"""
            SELECT COUNT(*)
            FROM fact_sales as f
            LEFT JOIN {dim} d
            ON f.{key} = d.{key}
            WHERE d.{key} IS NULL
        """
        )

        orphan_count, = db_cursor.fetchone()

        assert orphan_count == 0, f"{dim}.{key} has {orphan_count} orphan rows"

def test_fact_sales_has_valid_measures(db_cursor):
    # Profit can be zero because validation allows unit_cost == unit_price.
    db_cursor.execute("""
        SELECT COUNT(*)
        FROM fact_sales
        WHERE quantity <= 0
           OR revenue IS NULL
           OR profit IS NULL
           OR revenue <= 0
           OR profit < 0;
    """)

    invalid_count, = db_cursor.fetchone()

    assert invalid_count == 0