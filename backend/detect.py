import cv2
import pytesseract
import io
import requests
from PIL import Image
from ultralytics import YOLO
import numpy as np
import asyncio
import httpx

# Load YOLO model ONCE (Big performance boost)
model = YOLO("yolov8n.pt")

GOOGLE_BOOKS_API = "https://www.googleapis.com/books/v1/volumes?q="


# -----------------------------------------------------------
# 1) DETECT BOOK SPINES (Optimized)
# -----------------------------------------------------------
def detect_spines(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception:
        return []

    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # ⚡ Resize for speed
    img = cv2.resize(img, (640, 640))

    results = model(img, verbose=False)
    cropped_spines = []

    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # ⚡ Skip tiny crops (noise)
        if (x2 - x1) < 30 or (y2 - y1) < 80:
            continue

        crop = img[y1:y2, x1:x2]
        cropped_spines.append(crop)

    return cropped_spines


# -----------------------------------------------------------
# 2) OCR (Optimized)
# -----------------------------------------------------------
def extract_text(image):
    try:
        text = pytesseract.image_to_string(Image.fromarray(image))
        text = text.strip()

        # ⚡ Filter nonsense OCR
        if len(text) < 3:
            return None
        if not any(c.isalpha() for c in text):
            return None

        return text

    except Exception:
        return None


# -----------------------------------------------------------
# 3) ASYNC GOOGLE BOOKS CALL (Much faster)
# -----------------------------------------------------------
async def fetch_book(query):
    try:
        url = GOOGLE_BOOKS_API + query

        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url)
            data = r.json()

            if "items" not in data:
                return None

            info = data["items"][0]["volumeInfo"]

            return {
                "title": info.get("title", "Unknown"),
                "authors": info.get("authors", ["Unknown"]),
                "thumbnail": info.get("imageLinks", {}).get("thumbnail", ""),
                "summary": info.get("description", "No summary available"),
                "categories": info.get("categories", ["Uncategorized"]),
                "rating": info.get("averageRating", "N/A")
            }

    except Exception:
        return None


# -----------------------------------------------------------
# 4) MAIN FUNCTION — Optimized + Parallel API Calls
# -----------------------------------------------------------
def detect_books(image_bytes):
    spines = detect_spines(image_bytes)
    ocr_texts = []

    # OCR all crops
    for spine in spines:
        text = extract_text(spine)
        if text:
            ocr_texts.append(text)

    # ⚡ Run Google Books calls in parallel
    async def gather_books():
        tasks = [fetch_book(t) for t in ocr_texts]
        results = await asyncio.gather(*tasks)
        return [r for r in results if r]

    results = asyncio.run(gather_books())
    return results
