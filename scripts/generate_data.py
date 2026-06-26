from pathlib import Path
import random
from faker import Faker
import pandas as pd
from datetime import date, timedelta

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

# Make generated data reproducible
fake = Faker()
Faker.seed(4321)
random.seed(4321)

def generate_customers():
    """
    Generate synthetic customer data.

    City distribution is weighted so Amman customers appear more often.
    Segment distribution is weighted toward Regular customers, followed by
    Students and Business customers, with Premium customers being the rarest.
    """

    cities = ["Amman", "Amman", "Amman", "Amman","Irbid", "Zarqa", "Aqaba", "Salt", "Madaba", "Jerash"]

    segments = [
        "Regular", "Regular", "Regular","Regular",
        "Premium", "Student", "Student", "Student", "Business", "Business"
    ]

    customers = []

    for i in range(1, 101):
        customers.append({
            "customer_id" : f"C{i:04d}",
            "customer_name": fake.name(),
            "customer_city": random.choice(cities),
            "customer_segment": random.choice(segments)
        })

    customers_df = pd.DataFrame(customers)

    output_path = DATA_DIR / "customers.csv"
    customers_df.to_csv(output_path, index = False)
    
    print(f"Generated {len(customers)} customers at {output_path}")

    return customers_df

def generate_products():
    product_catalog = [
        # Electronics
        {"product_name": "Wireless Mouse", "category": "Electronics", "brand": "Logitech", "base_price": 18.99, "base_cost": 10.50},
        {"product_name": "Bluetooth Speaker", "category": "Electronics", "brand": "JBL", "base_price": 49.99, "base_cost": 28.00},
        {"product_name": "USB-C Cable", "category": "Electronics", "brand": "Anker", "base_price": 9.99, "base_cost": 3.50},
        {"product_name": "Laptop Stand", "category": "Electronics", "brand": "Ugreen", "base_price": 29.99, "base_cost": 14.00},
        {"product_name": "Power Bank", "category": "Electronics", "brand": "Anker", "base_price": 39.99, "base_cost": 22.00},
        {"product_name": "Wireless Keyboard", "category": "Electronics", "brand": "Logitech", "base_price": 34.99, "base_cost": 19.00},
        {"product_name": "HDMI Cable", "category": "Electronics", "brand": "Belkin", "base_price": 12.99, "base_cost": 5.00},
        {"product_name": "Phone Charger", "category": "Electronics", "brand": "Samsung", "base_price": 24.99, "base_cost": 11.00},

        # Clothing
        {"product_name": "Basic T-Shirt", "category": "Clothing", "brand": "H&M", "base_price": 14.99, "base_cost": 6.00},
        {"product_name": "Slim Fit Jeans", "category": "Clothing", "brand": "Levi's", "base_price": 59.99, "base_cost": 28.00},
        {"product_name": "Hoodie", "category": "Clothing", "brand": "Nike", "base_price": 54.99, "base_cost": 26.00},
        {"product_name": "Polo Shirt", "category": "Clothing", "brand": "Lacoste", "base_price": 69.99, "base_cost": 34.00},
        {"product_name": "Winter Jacket", "category": "Clothing", "brand": "Zara", "base_price": 89.99, "base_cost": 45.00},
        {"product_name": "Sweatpants", "category": "Clothing", "brand": "Adidas", "base_price": 44.99, "base_cost": 21.00},
        {"product_name": "Casual Shorts", "category": "Clothing", "brand": "H&M", "base_price": 24.99, "base_cost": 10.00},

        # Footwear
        {"product_name": "Running Shoes", "category": "Footwear", "brand": "Nike", "base_price": 79.99, "base_cost": 42.00},
        {"product_name": "Training Shoes", "category": "Footwear", "brand": "Adidas", "base_price": 74.99, "base_cost": 39.00},
        {"product_name": "Casual Sneakers", "category": "Footwear", "brand": "Vans", "base_price": 64.99, "base_cost": 31.00},
        {"product_name": "Leather Boots", "category": "Footwear", "brand": "Timberland", "base_price": 129.99, "base_cost": 70.00},
        {"product_name": "Slides", "category": "Footwear", "brand": "Adidas", "base_price": 29.99, "base_cost": 12.00},
        {"product_name": "Formal Shoes", "category": "Footwear", "brand": "Clarks", "base_price": 99.99, "base_cost": 52.00},

        # Grocery
        {"product_name": "Coffee Beans", "category": "Grocery", "brand": "Lavazza", "base_price": 11.99, "base_cost": 6.00},
        {"product_name": "Olive Oil", "category": "Grocery", "brand": "Al Ameed", "base_price": 8.99, "base_cost": 4.20},
        {"product_name": "Pasta Pack", "category": "Grocery", "brand": "Barilla", "base_price": 3.49, "base_cost": 1.50},
        {"product_name": "Rice Bag", "category": "Grocery", "brand": "Sunwhite", "base_price": 12.99, "base_cost": 7.00},
        {"product_name": "Cereal Box", "category": "Grocery", "brand": "Kellogg's", "base_price": 5.99, "base_cost": 2.80},
        {"product_name": "Chocolate Bar", "category": "Grocery", "brand": "Galaxy", "base_price": 1.49, "base_cost": 0.60},
        {"product_name": "Green Tea", "category": "Grocery", "brand": "Twinings", "base_price": 4.99, "base_cost": 2.10},
        {"product_name": "Peanut Butter", "category": "Grocery", "brand": "Skippy", "base_price": 6.49, "base_cost": 3.00},

        # Home
        {"product_name": "Desk Lamp", "category": "Home", "brand": "IKEA", "base_price": 24.99, "base_cost": 11.00},
        {"product_name": "Bed Sheets", "category": "Home", "brand": "IKEA", "base_price": 39.99, "base_cost": 18.00},
        {"product_name": "Kitchen Knife Set", "category": "Home", "brand": "Tefal", "base_price": 49.99, "base_cost": 25.00},
        {"product_name": "Nonstick Pan", "category": "Home", "brand": "Tefal", "base_price": 34.99, "base_cost": 16.00},
        {"product_name": "Storage Box", "category": "Home", "brand": "IKEA", "base_price": 14.99, "base_cost": 6.50},
        {"product_name": "Bath Towel", "category": "Home", "brand": "Home Centre", "base_price": 9.99, "base_cost": 4.00},

        # Beauty
        {"product_name": "Shampoo", "category": "Beauty", "brand": "Dove", "base_price": 5.99, "base_cost": 2.40},
        {"product_name": "Face Wash", "category": "Beauty", "brand": "Nivea", "base_price": 7.99, "base_cost": 3.20},
        {"product_name": "Body Lotion", "category": "Beauty", "brand": "Vaseline", "base_price": 6.99, "base_cost": 2.90},
        {"product_name": "Perfume", "category": "Beauty", "brand": "Calvin Klein", "base_price": 59.99, "base_cost": 30.00},
        {"product_name": "Sunscreen", "category": "Beauty", "brand": "La Roche-Posay", "base_price": 24.99, "base_cost": 13.00},

        # Sports
        {"product_name": "Yoga Mat", "category": "Sports", "brand": "Decathlon", "base_price": 19.99, "base_cost": 8.00},
        {"product_name": "Dumbbell Set", "category": "Sports", "brand": "Decathlon", "base_price": 49.99, "base_cost": 27.00},
        {"product_name": "Football", "category": "Sports", "brand": "Adidas", "base_price": 29.99, "base_cost": 14.00},
        {"product_name": "Resistance Bands", "category": "Sports", "brand": "Nike", "base_price": 14.99, "base_cost": 5.50},
        {"product_name": "Water Bottle", "category": "Sports", "brand": "Under Armour", "base_price": 12.99, "base_cost": 4.80},

        # Books
        {"product_name": "Python Programming Book", "category": "Books", "brand": "O'Reilly", "base_price": 44.99, "base_cost": 23.00},
        {"product_name": "SQL Fundamentals Book", "category": "Books", "brand": "Manning", "base_price": 39.99, "base_cost": 20.00},
        {"product_name": "Business Analytics Book", "category": "Books", "brand": "Pearson", "base_price": 49.99, "base_cost": 26.00},
        {"product_name": "Data Engineering Book", "category": "Books", "brand": "O'Reilly", "base_price": 54.99, "base_cost": 29.00},
        {"product_name": "Finance Basics Book", "category": "Books", "brand": "McGraw Hill", "base_price": 34.99, "base_cost": 17.00},
    ]

    products = []

    for i, product in enumerate(product_catalog, start=1):
        products.append({
            "product_id": f"P{i:04d}",
            "product_name": product["product_name"],
            "category": product["category"],
            "brand": product["brand"],
            "base_price": product["base_price"],
            "base_cost": product["base_cost"],
        })

    products_df = pd.DataFrame(products)

    output_path = DATA_DIR / "products.csv"

    products_df.to_csv(output_path, index=False)

    print(f"Generated {len(products_df)} products at {output_path}")

    return products_df

def generate_stores():
    stores = [
        {"store_id": "ST001", "store_name": "Amman Downtown Store", "store_city": "Amman"},
        {"store_id": "ST002", "store_name": "Irbid City Mall Store", "store_city": "Irbid"},
        {"store_id": "ST003", "store_name": "Zarqa Central Store", "store_city": "Zarqa"},
        {"store_id": "ST004", "store_name": "Aqaba Corniche Store", "store_city": "Aqaba"},
        {"store_id": "ST005", "store_name": "Salt Heritage Store", "store_city": "Salt"},
        {"store_id": "ST006", "store_name": "Madaba Market Store", "store_city": "Madaba"},
        {"store_id": "ST007", "store_name": "Jerash Plaza Store", "store_city": "Jerash"},
        {"store_id": "ST008", "store_name": "Amman Mecca Street Store", "store_city": "Amman"},
    ]
    
    stores_df = pd.DataFrame(stores)

    output_path = DATA_DIR / "stores.csv"
    stores_df.to_csv(output_path, index=False)

    print(f"Generated {len(stores_df)} stores at {output_path}")
    return stores_df

def generate_sales(customers_df, products_df, stores_df, num_sales=10000):
    sales = []

    start_date = date(2025, 1, 1)
    end_date = date(2026, 12, 31)
    date_range_days = (end_date - start_date).days

    for i in range(1, num_sales + 1):
        customer = customers_df.sample(1).iloc[0]
        product = products_df.sample(1).iloc[0]
        
        customer_local_store = stores_df[
            stores_df["store_city"] == customer["customer_city"]
        ]

        customer_external_store = stores_df[
            stores_df["store_city"] != customer["customer_city"]
        ]
        
        # Customers usually buy from stores in their own city, but sometimes from other cities
        if not customer_local_store.empty and random.random() < 0.8:
            store = customer_local_store.sample(1).iloc[0]
        else:
            store = customer_external_store.sample(1).iloc[0]

        # Generate a random sale date between start_date and end_date
        sale_date = start_date + timedelta(days=random.randint(0, date_range_days))

        quantity = random.randint(1, 5)

        # Vary unit price to simulate discounts, promotions, and occasional markupgit
        unit_price = round(product["base_price"] * random.uniform(0.85, 1.10), 2)
        # Vary unit cost slightly to simulate supplier cost changes
        unit_cost = round(product["base_cost"] * random.uniform(0.98, 1.05), 2)

        sale = {
            "sale_id": f"S{i:06d}",
            "customer_id": customer["customer_id"],
            "product_id": product["product_id"],
            "store_id": store["store_id"],
            "sale_date": sale_date.isoformat(),
            "quantity": quantity,
            "unit_price": unit_price,
            "unit_cost": unit_cost,
        }

        sales.append(sale)

    sales_df = pd.DataFrame(sales)

    output_path = DATA_DIR / "sales.csv"
    sales_df.to_csv(output_path, index=False)

    print(f"Generated {len(sales_df)} sales at {output_path}")

    return sales_df


if __name__ == "__main__":
    customers_df = generate_customers()
    products_df = generate_products()
    stores_df = generate_stores()
    generate_sales(customers_df, products_df, stores_df)