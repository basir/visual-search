import numpy as np
import cv2
from PIL import Image
from sklearn.cluster import MiniBatchKMeans
import time


# Define precise color ranges in HSV
COLOR_RANGES = {
    "red": [
        ((0, 70, 50), (10, 255, 255)),  # Pure red
        ((160, 70, 50), (180, 255, 255)),  # Deep red
    ],
    "orange": [((11, 70, 50), (25, 255, 255))],
    "yellow": [((26, 70, 50), (34, 255, 255))],
    "green": [((35, 70, 50), (85, 255, 255))],  # Pure green
    "blue": [((86, 70, 50), (130, 255, 255))],  # Pure blue
    "purple": [((131, 70, 50), (155, 255, 255))],  # Pure purple
    "pink": [((156, 70, 50), (170, 255, 255))],  # Pure pink
    "brown": [((0, 30, 20), (20, 200, 100))],  # Dark brown
    "white": [((0, 0, 220), (180, 30, 255))],
    "black": [((0, 0, 0), (180, 30, 40))],
    "gray": [((0, 0, 40), (180, 30, 220))],
    "beige": [((20, 10, 180), (40, 30, 255))],
}


def create_mask(image):
    """Create a simple mask for the main object using basic thresholding."""
    try:
        start_time = time.time()

        # Convert PIL Image to cv2 format
        img = np.array(image)

        # Ensure the image is not too large
        max_size = 200
        if max(img.shape[:2]) > max_size:
            scale = max_size / max(img.shape[:2])
            new_size = tuple(int(dim * scale) for dim in img.shape[:2][::-1])
            img = cv2.resize(img, new_size)

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # Simple binary thresholding
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # Find contours
        contours, _ = cv2.findContours(
            binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:
            return np.ones(img.shape[:2], dtype=np.uint8)

        # Create mask from all contours
        mask = np.zeros_like(gray)
        cv2.drawContours(mask, contours, -1, 255, -1)

        return mask > 0

    except Exception as e:
        return np.ones(img.shape[:2], dtype=np.uint8)


def get_dominant_color(image, n_colors=3):
    """Get the dominant color(s) of a clothing item in an image."""
    try:
        start_time = time.time()

        # Resize image for faster processing
        img = image.copy()
        img.thumbnail((100, 100))

        # Convert to numpy array
        img_array = np.array(img)

        # Convert to HSV
        img_hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)

        # Reshape for clustering
        pixels = img_hsv.reshape(-1, 3)

        # Use MiniBatchKMeans for faster processing
        kmeans = MiniBatchKMeans(
            n_clusters=n_colors, batch_size=100, random_state=42, n_init=1, max_iter=10
        )

        kmeans.fit(pixels)

        # Get color percentages
        colors = kmeans.cluster_centers_
        labels = kmeans.labels_
        percentages = np.bincount(labels) / len(labels)

        # Match colors to predefined ranges
        matched_colors = {}

        for color, percentage in zip(colors, percentages):
            h, s, v = color

            # Quick check for grayscale
            if s < 30 or v < 30 or v > 240:
                if v > 200:
                    matched_colors["white"] = (
                        matched_colors.get("white", 0) + percentage
                    )
                elif v < 50:
                    matched_colors["black"] = (
                        matched_colors.get("black", 0) + percentage
                    )
                else:
                    matched_colors["gray"] = matched_colors.get("gray", 0) + percentage
                continue

            # Match with color ranges
            for color_name, ranges in COLOR_RANGES.items():
                for (h_min, s_min, v_min), (h_max, s_max, v_max) in ranges:
                    if color_name == "red":  # Special case for red
                        in_range = (
                            ((0 <= h <= 10) or (160 <= h <= 180))
                            and s >= 70
                            and v >= 50
                        )
                    else:
                        in_range = (
                            h_min <= h <= h_max
                            and s_min <= s <= s_max
                            and v_min <= v <= v_max
                        )

                    if in_range:
                        matched_colors[color_name] = (
                            matched_colors.get(color_name, 0) + percentage
                        )
                        break

        if not matched_colors:
            return "other"

        # Sort colors by percentage
        sorted_colors = sorted(matched_colors.items(), key=lambda x: x[1], reverse=True)

        # Return the dominant color
        if sorted_colors[0][1] > 0.4:  # Lowered threshold
            return sorted_colors[0][0]
        elif (
            len(sorted_colors) >= 2
            and sorted_colors[0][1] > 0.3
            and sorted_colors[1][1] > 0.2
        ):
            return "other"

        return sorted_colors[0][0]

    except Exception as e:
        return "other"
