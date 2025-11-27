# Use PyTorch CPU image (has correct torch preinstalled)
FROM pytorch/pytorch:2.3.1-cpu

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 libxext6 libxrender1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies (torch already included)
RUN pip install --upgrade pip \
    && pip install --no-cache-dir fastapi uvicorn[standard] \
    pillow requests pytesseract numpy \
    opencv-python-headless ultralytics==8.3.3

# Copy project code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
