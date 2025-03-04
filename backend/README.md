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
