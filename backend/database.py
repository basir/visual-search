import sqlite3
import json
import numpy as np
from typing import List, Dict, Any
import os
from config import DB_PATH


def init_db():
    """Initialize the database with required tables."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create products table
    c.execute("""CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY,
                  name TEXT,
                  price REAL,
                  image_url TEXT,
                  category TEXT,
                  color TEXT)""")

    # Create product_features table
    c.execute("""CREATE TABLE IF NOT EXISTS product_features
                 (product_id INTEGER PRIMARY KEY,
                  features BLOB)""")

    conn.commit()
    conn.close()


def save_products(products: List[Dict[str, Any]]):
    """Save products to database. Skip if product already exists."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    for product in products:
        c.execute(
            """INSERT OR IGNORE INTO products (id, name, price, image_url)
                     VALUES (?, ?, ?, ?)""",
            (product["id"], product["name"], product["price"], product["image_url"]),
        )

    conn.commit()
    conn.close()


def load_products() -> List[Dict[str, Any]]:
    """Load products from database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT * FROM products")
    rows = c.fetchall()

    products = []
    for row in rows:
        product = {
            "id": row[0],
            "name": row[1],
            "price": row[2],
            "image_url": row[3],
            "category": row[4],
            "color": row[5],
        }
        products.append(product)

    conn.close()
    return products


def save_product_features(product_id: int, features: np.ndarray):
    """Save product features to database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Convert numpy array to bytes for storage
    feature_bytes = features.tobytes()

    c.execute(
        """INSERT OR REPLACE INTO product_features (product_id, features)
                 VALUES (?, ?)""",
        (product_id, feature_bytes),
    )

    conn.commit()
    conn.close()


def load_product_features() -> Dict[int, np.ndarray]:
    """Load product features from database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT product_id, features FROM product_features")
    rows = c.fetchall()

    features = {}
    for row in rows:
        product_id = row[0]
        # Convert bytes back to numpy array
        feature_array = np.frombuffer(row[1], dtype=np.float32)
        # Reshape to match the expected feature dimensions
        feature_array = feature_array.reshape(1, -1)
        features[product_id] = feature_array

    conn.close()
    return features


def update_product_attributes(product_id: int, category: str, color: str):
    """Update product category and color."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        """UPDATE products 
                 SET category = ?, color = ?
                 WHERE id = ?""",
        (category, color, product_id),
    )

    conn.commit()
    conn.close()


def update_product_image_url(product_id: int, image_url: str):
    """Update product image URL."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        """UPDATE products 
                 SET image_url = ?
                 WHERE id = ?""",
        (image_url, product_id),
    )

    conn.commit()
    conn.close()
