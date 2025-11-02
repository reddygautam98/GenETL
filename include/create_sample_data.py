import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

# Set seed for reproducible results
np.random.seed(42)
random.seed(42)

# Define product data
categories = [
    "Electronics",
    "Clothing",
    "Books",
    "Home & Garden",
    "Sports",
    "Beauty",
    "Automotive",
    "Toys",
]
brands = [
    "BrandA",
    "BrandB",
    "BrandC",
    "BrandD",
    "BrandE",
    "BrandF",
    "BrandG",
    "BrandH",
]

product_types = {
    "Electronics": [
        "Smartphone",
        "Laptop",
        "Tablet",
        "Headphones",
        "Camera",
        "TV",
        "Speaker",
        "Watch",
    ],
    "Clothing": [
        "T-Shirt",
        "Jeans",
        "Dress",
        "Jacket",
        "Shoes",
        "Hat",
        "Sweater",
        "Socks",
    ],
    "Books": [
        "Novel",
        "Textbook",
        "Cookbook",
        "Biography",
        "Science Fiction",
        "Mystery",
        "Romance",
        "History",
    ],
    "Home & Garden": [
        "Chair",
        "Table",
        "Lamp",
        "Vase",
        "Plant",
        "Tool",
        "Cushion",
        "Rug",
    ],
    "Sports": [
        "Ball",
        "Racket",
        "Shoes",
        "Shirt",
        "Equipment",
        "Bag",
        "Bottle",
        "Gloves",
    ],
    "Beauty": [
        "Lipstick",
        "Foundation",
        "Perfume",
        "Shampoo",
        "Cream",
        "Mascara",
        "Lotion",
        "Soap",
    ],
    "Automotive": [
        "Tire",
        "Battery",
        "Oil",
        "Filter",
        "Light",
        "Mirror",
        "Seat Cover",
        "Mat",
    ],
    "Toys": ["Doll", "Car", "Puzzle", "Game", "Ball", "Bear", "Block", "Robot"],
}

# Generate 5000 product records
n_products = 5000
data = []

print(f"Generating {n_products} product records...")

for i in range(1, n_products + 1):
    category = random.choice(categories)
    brand = random.choice(brands)
    product_type = random.choice(product_types[category])

    # Set price based on category
    if category == "Electronics":
        price = round(random.uniform(50.0, 2000.0), 2)
    elif category == "Automotive":
        price = round(random.uniform(20.0, 500.0), 2)
    elif category == "Books":
        price = round(random.uniform(5.0, 50.0), 2)
    else:
        price = round(random.uniform(10.0, 300.0), 2)

    # Generate random dates
    created_days = random.randint(0, 365)
    created_hours = random.randint(0, 23)
    created_date = datetime(2023, 1, 1) + timedelta(
        days=created_days, hours=created_hours
    )

    update_days = random.randint(0, 100)
    update_hours = random.randint(0, 23)
    last_updated = created_date + timedelta(days=update_days, hours=update_hours)

    row = {
        "product_id": i,
        "product_name": f"{brand} {product_type} {i % 100}",
        "category": category,
        "brand": brand,
        "price": price,
        "quantity_in_stock": random.randint(0, 1000),
        "supplier_id": random.randint(1, 100),
        "created_date": created_date.strftime("%Y-%m-%d %H:%M:%S"),
        "last_updated": last_updated.strftime("%Y-%m-%d %H:%M:%S"),
        "is_active": random.choice([True, False]),
        "rating": round(random.uniform(1.0, 5.0), 1),
        "description": f"High quality {product_type.lower()} from {brand} in {category.lower()} category. Product ID: {i}",
    }
    data.append(row)

    if i % 1000 == 0:
        print(f"Generated {i} records...")

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
output_file = "include/products_sample_5000.csv"
df.to_csv(output_file, index=False)

print(f"Successfully generated {len(df)} product records!")
print(f"Categories: {df['category'].nunique()} unique categories")
print(f"Brands: {df['brand'].nunique()} unique brands")
print(f"Price range: ${df['price'].min():.2f} - ${df['price'].max():.2f}")
print(f"Average price: ${df['price'].mean():.2f}")
print(f"Active products: {df['is_active'].sum()}")
print(f"File saved: {output_file}")
print(f"File size: {len(df)} rows, {len(df.columns)} columns")
