FROM python:3.10-slim

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies for PyTorch + Tesseract + OpenCV
RUN apt-get update && apt-get install -y \
    git wget curl nano \
    libgl1 libglib2.0-0 libsm6 libxext6 libxrender1 \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Install requirements first (this keeps cache efficient)
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Gunicorn + Uvicorn worker server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
