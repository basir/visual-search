import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import hashlib
from pathlib import Path
import logging
from config import IMAGE_CACHE_DIR

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Image transformation
transform = transforms.Compose(
    [
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)


def get_model():
    """Load the pre-trained ResNet model."""
    model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
    # Remove the classification layer
    model = torch.nn.Sequential(*list(model.children())[:-1])
    model.eval()
    return model


def extract_features(image, model):
    """Extract features from an image using the model."""
    image_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        features = model(image_tensor)
    return features.squeeze().numpy()


def get_cached_image(url: str) -> Image.Image:
    """Get image from cache if it exists, otherwise return None."""
    url_hash = hashlib.md5(url.encode()).hexdigest()
    cache_path = Path(IMAGE_CACHE_DIR) / f"{url_hash}.jpg"

    if cache_path.exists():
        try:
            return Image.open(cache_path).convert("RGB")
        except Exception as e:
            logger.error(f"Error loading cached image: {str(e)}")
            return None
    return None


def cache_image(url: str, image: Image.Image) -> None:
    """Save image to cache."""
    try:
        url_hash = hashlib.md5(url.encode()).hexdigest()
        cache_path = Path(IMAGE_CACHE_DIR) / f"{url_hash}.jpg"
        image.save(cache_path, "JPEG")
    except Exception as e:
        logger.error(f"Error caching image: {str(e)}")


# Initialize model
model = get_model()
