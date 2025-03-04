import os

# Set tokenizers parallelism before importing any HuggingFace libraries
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
import json
from PIL import Image
import io
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from contextlib import asynccontextmanager
from urllib.request import urlopen
from database import (
    init_db,
    load_products,
    save_products,
    save_product_features,
    load_product_features,
    update_product_attributes,
    update_product_image_url,
)
from pathlib import Path
from fashion_classifier import create_classifier
from color_classifier import get_dominant_color
from image_utils import get_cached_image, cache_image, extract_features, model
import logging
from config import PRODUCTS_FILE

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the fashion classifier
fashion_classifier = None


async def initialize_models():
    """Initialize all ML models before starting product processing."""
    global fashion_classifier
    logger.info("Initializing fashion classifier...")
    fashion_classifier = create_classifier()
    logger.info("Fashion classifier initialized successfully")


async def get_product_category(image: Image.Image) -> Dict[str, Any]:
    """Get the product category using the fashion classifier."""
    global fashion_classifier

    try:
        # Get prediction from the classifier
        logger.info("Getting prediction from fashion classifier")
        category, confidence = fashion_classifier.predict(image)
        logger.info(f"Predicted category: {category} with confidence: {confidence}")
        return {"category": category, "confidence": confidence}
    except Exception as e:
        logger.error(f"Error in fashion classification: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Error in fashion classification: {str(e)}"
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\nStarting application initialization...")

    try:
        # Initialize database
        init_db()

        # Initialize ML models first
        print("Initializing ML models...")
        await initialize_models()
        print("ML models initialized successfully")

        print("\nStarting product processing...")
        # Load products from database
        json_products = load_products_json()
        # json_products = json_products[:5]
        save_products(json_products)
        products = load_products()
        print(f"Total products to process: {len(products)}")

        # Load existing product features
        product_features = load_product_features()

        # Process each product
        for product in products:
            print(f"\nProcessing product {product['id']}: {product['name']}")

            # Check if product features already exist
            if product["id"] not in product_features:
                try:
                    image = get_cached_image(product["image_url"])

                    if image is None:
                        print(f"- Downloading image")
                        with urlopen(product["image_url"]) as response:
                            image = Image.open(response).convert("RGB")
                    else:
                        print("- Using cached image")

                    # Extract features for similarity search
                    print("- Extracting features for similarity search")
                    features = extract_features(image, model)
                    product_features[product["id"]] = features

                    # Infer category and color
                    category_result = await get_product_category(image)
                    color = get_dominant_color(image)

                    print(
                        f"- Detected category: {category_result['category']}, color: {color}"
                    )

                    # Update product attributes
                    print("- Updating product attributes in database")
                    update_product_attributes(
                        product["id"], category_result["category"], color
                    )

                    # Save features to database
                    print("- Saving features to database")
                    save_product_features(product["id"], features)

                    print(f"✓ Successfully processed product {product['id']}")

                except Exception as e:
                    print(f"✗ Error processing product {product['id']}: {str(e)}")
            else:
                print(f"- Product {product['id']} already processed, skipping")

        print("\nProduct processing completed!")
        yield
    except Exception as e:
        yield


app = FastAPI(title="Visual Search API", lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Sample products data
PRODUCTS_FILE = "data/products.json"

# Initialize with sample data if file doesn't exist
if not os.path.exists(PRODUCTS_FILE):
    raise FileNotFoundError(f"File {PRODUCTS_FILE} not found")


# Load products.json
def load_products_json():
    with open(PRODUCTS_FILE, "r") as f:
        return json.load(f)


# Feature cache
product_features = {}


@app.get("/api/products")
async def get_products():
    return load_products()


@app.get("/api/search/text")
async def search_by_text(query: str):
    products = load_products()
    if not query:
        return products

    # Simple case-insensitive search in product names
    results = [p for p in products if query.lower() in p["name"].lower()]
    return results


@app.post("/api/search/image")
async def search_by_image(
    file: UploadFile = File(...), similarity_threshold: float = 0.5
):
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        # Read and process the uploaded image
        contents = await file.read()
        try:
            image = Image.open(io.BytesIO(contents)).convert("RGB")
        except Exception as e:
            logger.error(f"Error opening image: {str(e)}")
            raise HTTPException(status_code=400, detail="Invalid image file")

        # Extract features from the uploaded image
        try:
            query_features = extract_features(image, model)
        except Exception as e:
            logger.error(f"Error extracting features: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error processing image features"
            )

        # Compare with pre-computed product features
        products = load_products()
        similarities = []

        # Load features from database
        try:
            product_features = load_product_features()
        except Exception as e:
            logger.error(f"Error loading product features: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error loading product database"
            )

        for product in products:
            if product["id"] in product_features:
                try:
                    # Ensure features are properly shaped numpy arrays
                    query_feat = np.array(query_features).reshape(1, -1)
                    prod_feat = np.array(product_features[product["id"]]).reshape(1, -1)

                    similarity = cosine_similarity(query_feat, prod_feat)[0][0]
                    if similarity >= similarity_threshold:
                        similarities.append((product, float(similarity)))
                except Exception as e:
                    logger.error(
                        f"Error calculating similarity for product {product['id']}: {str(e)}"
                    )
                    continue

        # Sort by similarity (highest first)
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Return the top results
        results = [item[0] for item in similarities]

        if not results:
            logger.info("No similar products found")
            return []

        return results

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Unexpected error in search_by_image: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error processing request: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
