FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create directories for cache and data with proper permissions
RUN mkdir -p /app/data/image_cache && \
    mkdir -p /root/.cache/torch/hub/checkpoints/ && \
    mkdir -p /root/.cache/huggingface/ && \
    chmod -R 777 /app/data

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TORCH_HOME=/root/.cache/torch
ENV TRANSFORMERS_CACHE=/root/.cache/huggingface
ENV APP_DATA_DIR=/app/data
# Optimize for CPU
ENV TORCH_CPU_PARALLEL=1
ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1
# Filter out the huggingface deprecation warning
ENV PYTHONWARNINGS="ignore::FutureWarning:huggingface_hub.file_download"

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application with debug logging
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"]