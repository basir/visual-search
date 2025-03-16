# Visual Search Application

A full-stack application for visual search capabilities, built with Next.js frontend and FastAPI backend.

## Quick Start

### Prerequisites

- Docker
- Docker Compose

### Running the Application

1. Clone the repository
2. From the root directory, run:

```bash
docker-compose up --build
```

This will start both the frontend and backend services:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Development Setup

### Frontend (Next.js)

For local development of the frontend:

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

### Backend (FastAPI)

For local development of the backend:

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Navigate to the backend directory:

```bash
cd backend
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the development server:

```bash
uvicorn main:app --reload
```

## Architecture

- Frontend: Next.js application with TypeScript
- Backend: FastAPI application with Python
- Image Processing: PyTorch, OpenCV, and Transformers
- API Documentation: Swagger UI and ReDoc

## Notes

- The frontend is configured to proxy API requests to the backend
- Both services use Docker for production deployment
- The backend uses CPU-only versions of PyTorch for compatibility
- Development can be done either with Docker or locally
