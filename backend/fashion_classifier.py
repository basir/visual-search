import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
from typing import Tuple
import numpy as np
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FashionClassifier:
    _instance = None
    _is_initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FashionClassifier, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._is_initialized:
            logger.info("Initializing FashionClassifier...")
            # Load smaller CLIP model
            self.model_name = "openai/clip-vit-base-patch16"

            # Check if model is already in cache
            cache_dir = os.environ.get("TRANSFORMERS_CACHE")
            if not cache_dir:
                # If not running in Docker, use local cache
                cache_dir = os.path.join(
                    os.path.expanduser("~"), ".cache", "huggingface"
                )
                os.makedirs(cache_dir, exist_ok=True)
            logger.info(f"Using cache directory: {cache_dir}")

            try:
                logger.info("Loading CLIP model and processor...")
                self.model = CLIPModel.from_pretrained(
                    self.model_name, cache_dir=cache_dir
                )
                self.processor = CLIPProcessor.from_pretrained(
                    self.model_name, cache_dir=cache_dir
                )
                logger.info("Successfully loaded CLIP model and processor")
            except Exception as e:
                logger.error(f"Error loading CLIP model: {str(e)}")
                raise

            # Force model to CPU mode
            self.model = self.model.to("cpu")
            self.model.eval()

            # Define text descriptions for each category
            self.category_descriptions = {
                "tops": [
                    "a t-shirt",
                    "a casual shirt",
                    "a formal shirt",
                    "a blouse",
                    "a sweater",
                    "a tank top",
                    "a crop top",
                    "a polo shirt",
                ],
                "bottoms": [
                    "pants",
                    "jeans",
                    "trousers",
                    "shorts",
                    "a skirt",
                    "denim pants",
                    "cargo pants",
                    "casual pants",
                ],
                "dresses": [
                    "a dress",
                    "a maxi dress",
                    "a mini dress",
                    "an evening dress",
                    "a casual dress",
                    "a formal dress",
                    "a cocktail dress",
                ],
                "outerwear": [
                    "a jacket",
                    "a coat",
                    "a blazer",
                    "a cardigan",
                    "a leather jacket",
                    "a denim jacket",
                    "a winter coat",
                ],
                "activewear": [
                    "workout clothes",
                    "gym clothes",
                    "sports clothing",
                    "athletic wear",
                    "training clothes",
                    "yoga clothes",
                ],
                "shoes": [
                    "shoes",
                    "sneakers",
                    "boots",
                    "sandals",
                    "heels",
                    "athletic shoes",
                    "casual shoes",
                    "formal shoes",
                ],
                "accessories": [
                    "a bag",
                    "a handbag",
                    "jewelry",
                    "a hat",
                    "a scarf",
                    "a belt",
                    "sunglasses",
                    "fashion accessories",
                ],
            }

            self._is_initialized = True
            logger.info("FashionClassifier initialization complete")

    def predict(self, image: Image.Image) -> Tuple[str, float]:
        try:
            # Prepare image
            inputs = self.processor(
                images=image,
                text=[
                    desc
                    for descs in self.category_descriptions.values()
                    for desc in descs
                ],
                return_tensors="pt",
                padding=True,
            )

            # Move tensors to CPU and ensure correct types
            for key in inputs:
                if torch.is_tensor(inputs[key]):
                    if key == "pixel_values":
                        inputs[key] = inputs[key].to("cpu").float()
                    else:
                        inputs[key] = inputs[key].to("cpu").long()

            # Process image and text separately
            with torch.no_grad():
                # Get image features
                image_features = self.model.get_image_features(inputs["pixel_values"])

                # Get text features
                text_features = self.model.get_text_features(
                    input_ids=inputs["input_ids"],
                    attention_mask=inputs["attention_mask"],
                )

                # Normalize features
                image_features = image_features / image_features.norm(
                    dim=-1, keepdim=True
                )
                text_features = text_features / text_features.norm(dim=-1, keepdim=True)

                # Calculate similarity scores using einsum instead of matmul
                logit_scale = self.model.logit_scale.exp()
                similarity = (
                    torch.einsum("bd,nd->bn", image_features, text_features)
                    * logit_scale
                )

                # Get probabilities
                probs = torch.nn.functional.softmax(similarity[0], dim=0)

            # Aggregate probabilities for each category
            category_scores = {}
            idx = 0
            for category, descriptions in self.category_descriptions.items():
                category_probs = probs[idx : idx + len(descriptions)]
                category_scores[category] = float(torch.max(category_probs))
                idx += len(descriptions)

            # Get the best category and its confidence
            best_category = max(category_scores.items(), key=lambda x: x[1])

            # Apply confidence threshold
            if best_category[1] >= 0.25:
                return best_category[0], best_category[1]

            return "other", best_category[1]

        except Exception as e:
            print(f"Error in prediction: {str(e)}")
            return "other", 0.0


def create_classifier() -> FashionClassifier:
    """Create and return a FashionClassifier instance"""
    return FashionClassifier()
