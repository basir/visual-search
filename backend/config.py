import os
from pathlib import Path

# Get base data directory from environment variable or use default
BASE_DATA_DIR = os.environ.get("APP_DATA_DIR", "data")

# Ensure base data directory exists
os.makedirs(BASE_DATA_DIR, exist_ok=True)

# Define specific paths
DB_PATH = os.path.join(BASE_DATA_DIR, "products.db")
IMAGE_CACHE_DIR = os.path.join(BASE_DATA_DIR, "image_cache")
PRODUCTS_FILE = os.path.join(BASE_DATA_DIR, "products.json")

# Ensure image cache directory exists
os.makedirs(IMAGE_CACHE_DIR, exist_ok=True)
