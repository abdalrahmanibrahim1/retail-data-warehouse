import psycopg2
from dotenv import load_dotenv
import os
from src.extract import extract_all
from src.validate import validate_all
from src.transform import transform_all

def get_connection():
    load_dotenv()

    conn = psycopg2.connect(
        host = os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user= os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
        )
    
    return conn

def create_tables(cursor):
    with open("schema.sql", 'r') as file:
        schema_sql = file.read()

    cursor.execute(schema_sql)

def clear_tables(cursor):
    cursor.execute("""
        TRUNCATE TABLE fact_sales, dim_customer, dim_product, dim_store, dim_date RESTART IDENTITY CASCADE;
    """)

def load_dim_customer(dim_customer, cursor):
    for _, row in dim_customer.iterrows():
        cursor.execute("""
            INSERT INTO dim_customer (
                customer_key,
                customer_id,
                customer_name,
                customer_city,
                customer_segment
            ) VALUES (%s, %s, %s, %s, %s);
            """, 
            (
                row["customer_key"], 
                row["customer_id"],
                row["customer_name"],
                row["customer_city"],
                row["customer_segment"]
            )
        )
        
    cursor.execute("SELECT count(*)  FROM dim_customer;")
    row_count = cursor.fetchone()
    if len(dim_customer) == row_count[0]:
        print("All customers loaded in successfully")
    else:
        raise ValueError("Customer load failed: row count mismatch")

def load_dim_product(dim_product, cursor):
    for _, row in dim_product.iterrows():
        cursor.execute("""
            INSERT INTO dim_product (
                product_key,
                product_id,
                product_name,
                category,
                brand
            ) VALUES (%s, %s, %s, %s, %s);
            """,
            (
                row["product_key"],
                row["product_id"],
                row["product_name"],
                row["category"],
                row["brand"]
            )
        )
    
    cursor.execute("SELECT COUNT(*) FROM dim_product;")
    row_count = cursor.fetchone()

    if len(dim_product) == row_count[0]:
        print("All products loaded successfully")
    else:
        raise ValueError("Products load failed: row count mismatch")

def load_dim_store(dim_store, cursor):
    for _, row in dim_store.iterrows():
        cursor.execute("""
            INSERT INTO dim_store (
                store_key,
                store_id,
                store_name,
                store_city
            ) VALUES (%s, %s, %s, %s);
            """,
            (
                row["store_key"],
                row["store_id"],
                row["store_name"],
                row["store_city"]
            )
        )
    
    cursor.execute("SELECT COUNT(*) FROM dim_store;")
    row_count = cursor.fetchone()

    if len(dim_store) == row_count[0]:
        print("All stores loaded successfully")
    else:
        raise ValueError("Stores load failed: row count mismatch")

def load_dim_date(dim_date, cursor):
    for _, row in dim_date.iterrows():
        cursor.execute("""
            INSERT INTO dim_date (
                date_key,
                full_date,
                year,
                quarter,
                month,
                day,
                weekday
            ) VALUES (%s, %s, %s, %s, %s, %s, %s);
            """,
            (
                row["date_key"],
                row["full_date"],
                row["year"],
                row["quarter"],
                row["month"],
                row["day"],
                row["weekday"]
            )
        )
    
    cursor.execute("SELECT COUNT(*) FROM dim_date;")
    row_count = cursor.fetchone()

    if len(dim_date) == row_count[0]:
        print("All dates loaded successfully")
    else:
        raise ValueError("Dates load failed: row count mismatch")

def load_fact_sales(fact_sales, cursor):
    for _, row in fact_sales.iterrows():
        cursor.execute("""
            INSERT INTO fact_sales (
                sale_key,
                sale_id,
                customer_key,
                product_key,
                store_key,
                date_key,
                quantity,
                revenue,
                profit
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """,
            (
                row["sale_key"],
                row["sale_id"],
                row["customer_key"],
                row["product_key"],
                row["store_key"],
                row["date_key"],
                row["quantity"],
                row["revenue"],
                row["profit"],
            )
        )
    
    cursor.execute("SELECT COUNT(*) FROM fact_sales;")
    row_count = cursor.fetchone()

    if len(fact_sales) == row_count[0]:
        print("All sales loaded successfully")
    else:
        raise ValueError("Sales load failed: row count mismatch")
    
def load_all(transformed_data):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        create_tables(cursor)
        clear_tables(cursor)
        load_dim_customer(transformed_data["dim_customer"], cursor)
        load_dim_product(transformed_data["dim_product"], cursor)
        load_dim_store(transformed_data["dim_store"], cursor)
        load_dim_date(transformed_data["dim_date"], cursor)
        load_fact_sales(transformed_data["fact_sales"], cursor)

        conn.commit()
        print("Warehouse load completed succesfully")
    except:
        conn.rollback()
        print("Warehouse load failed. Changes were rolled back.")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    data = extract_all()
    valid_data, invalid_data = validate_all(
        data["customers"],
        data["products"],
        data["stores"],
        data["sales"]
    )
    transformed_data = transform_all(valid_data)

    load_all(transformed_data)