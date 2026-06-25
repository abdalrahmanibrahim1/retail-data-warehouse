CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id VARCHAR(50) UNIQUE NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    customer_city VARCHAR(100) NOT NULL,
    customer_segment VARCHAR(50) NOT NULL
);


CREATE TABLE IF NOT EXISTS dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id VARCHAR(50) UNIQUE NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    brand VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_store (
	store_key SERIAL PRIMARY KEY,
	store_id VARCHAR(50) UNIQUE NOT NULL,
	store_name VARCHAR(100) NOT NULL,
	store_city VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE UNIQUE NOT NULL,
    year INT NOT NULL,
    quarter INT NOT NULL CHECK (quarter BETWEEN 1 AND 4),
    month INT NOT NULL CHECK (month BETWEEN 1 AND 12),
    day INT NOT NULL CHECK (day BETWEEN 1 AND 31),
    weekday VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS fact_sales (
    sale_key SERIAL PRIMARY KEY,
    sale_id VARCHAR(50) UNIQUE NOT NULL,

    customer_key INT NOT NULL,
    product_key INT NOT NULL,
    store_key INT NOT NULL,
    date_key INT NOT NULL,

    quantity INT NOT NULL CHECK (quantity > 0),
    revenue NUMERIC(12, 2) NOT NULL CHECK (revenue >= 0),
    profit NUMERIC(12, 2) NOT NULL,

    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (store_key) REFERENCES dim_store(store_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);