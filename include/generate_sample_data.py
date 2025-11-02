"""
Sample CSV Data Generator for GenETL Products Pipeline
Creates a CSV file with ~5000 product records for testing
"""

import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


def generate_sample_data():
    """Generate sample product data with 5000 rows"""

    # Set seed for reproducible data
    np.random.seed(42)

    # Define data categories
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

    # Product names by category
    product_names = {
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

    # Generate 5000 products
    n_products = 5000
    data_rows = []

    for i in range(1, n_products + 1):
        category = np.random.choice(categories)
        brand = np.random.choice(brands)
        product_type = np.random.choice(product_names[category])

        # Create realistic product name
        product_name = f"{brand} {product_type} {i % 100}"

        # Generate price based on category
        if category == "Electronics":
            price = np.round(np.random.uniform(50.00, 2000.00), 2)
        elif category == "Automotive":
            price = np.round(np.random.uniform(20.00, 500.00), 2)
        elif category == "Books":
            price = np.round(np.random.uniform(5.00, 50.00), 2)
        else:
            price = np.round(np.random.uniform(10.00, 300.00), 2)

        # Generate random dates
        created_date = datetime(2023, 1, 1) + timedelta(
            days=np.random.randint(0, 365), hours=np.random.randint(0, 24)
        )

        last_updated = created_date + timedelta(
            days=np.random.randint(0, 100), hours=np.random.randint(0, 24)
        )

        # Create data row
        row = {
            "product_id": i,
            "product_name": product_name,
            "category": category,
            "brand": brand,
            "price": price,
            "quantity_in_stock": np.random.randint(0, 1000),
            "supplier_id": np.random.randint(1, 100),
            "created_date": created_date.strftime("%Y-%m-%d %H:%M:%S"),
            "last_updated": last_updated.strftime("%Y-%m-%d %H:%M:%S"),
            "is_active": np.random.choice([True, False], p=[0.85, 0.15]),
            "rating": np.round(np.random.uniform(1.0, 5.0), 1),
            "description": f"High quality {product_type.lower()} from {brand} in {category.lower()} category. Product ID: {i}",
        }

        data_rows.append(row)

    return pd.DataFrame(data_rows)


if __name__ == "__main__":
    # Generate the data
    df = generate_sample_data()

    # Save to CSV
    output_file = "products_sample_5000.csv"
    df.to_csv(output_file, index=False)

    print(f"Generated {len(df)} product records")
    print(f"Saved to: {output_file}")
    print(f"File size: {os.path.getsize(output_file)} bytes")

    # Display sample data
    print("\nFirst 10 rows:")
    print(df.head(10).to_string())

    # Display statistics
    print(f"\nData Statistics:")
    print(f"Categories: {df['category'].nunique()} unique")
    print(f"Brands: {df['brand'].nunique()} unique")
    print(f"Price range: ${df['price'].min():.2f} - ${df['price'].max():.2f}")
    print(f"Average price: ${df['price'].mean():.2f}")
    print(f"Active products: {df['is_active'].sum()}")
    print(f"Date range: {df['created_date'].min()} to {df['created_date'].max()}")
