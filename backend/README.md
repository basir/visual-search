# Visual Search Backend

This is the backend service for the Visual Search project. It provides image processing and search capabilities using FastAPI.

## Requirements

- Docker and Docker Compose (recommended)
- Python 3.9+ (if running without Docker)

## Quick Start with Docker (Recommended)

1. Clone the repository
2. Navigate to the backend directory
3. Run the following command:

```bash
docker-compose up --build
```

The server will be available at `http://localhost:8000`

## Manual Setup (Alternative)

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the server:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access:

- API documentation: `http://localhost:8000/docs`
- Alternative API documentation: `http://localhost:8000/redoc`

## Troubleshooting

1. If you encounter memory issues with Docker, adjust the memory limit in Docker settings
2. For OpenCV-related errors, ensure system dependencies are installed:

   ```bash
   # Ubuntu/Debian
   sudo apt-get update && sudo apt-get install -y libgl1-mesa-glx libglib2.0-0

   # macOS
   brew install pkg-config
   ```

3. For PyTorch issues, the requirements.txt uses CPU-only versions by default for compatibility

## Notes

- The backend uses CPU-only versions of PyTorch for maximum compatibility
- All image processing is done on the CPU to ensure consistent behavior across different systems
- The server is configured to run on all network interfaces (0.0.0.0) by default

## Packages

Here's a brief explanation of each package in your backend/requirements.txt file:

- FastAPI (0.104.1): Modern, high-performance web framework for building APIs with Python, known for its speed and automatic documentation generation

- Uvicorn (0.24.0): ASGI server that runs your FastAPI application in production, handling HTTP requests efficiently

- Python-multipart (0.0.6): Enables handling of multipart form data, essential for file uploads in your API

- Pillow (10.1.0): Python Imaging Library fork that provides image processing capabilities

- NumPy (1.26.2): Fundamental package for scientific computing with Python, providing support for arrays, matrices, and mathematical functions

- PyTorch (2.1.1): Deep learning framework that offers tensor computation with GPU acceleration and tools for building neural networks

- TorchVision (0.16.1): Computer vision library built on PyTorch, containing datasets, model architectures, and image transformations

- Scikit-learn (1.3.2): Machine learning library providing simple tools for data analysis and modeling, including clustering and classification

- OpenCV-Python (4.8.1.78): Computer vision library with algorithms for image processing, object detection, and feature extraction

- Transformers (4.35.2): Hugging Face library providing state-of-the-art models for NLP and computer vision tasks, focusing on transformer architecture

These packages together form a powerful stack for a visual search application, combining web API capabilities with advanced computer vision and machine learning tools.
