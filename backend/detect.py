# detect.py
import cv2
import pytesseract
import io
import requests
from PIL import Image
from ultralytics import YOLO
import numpy as np

model = YOLO("yolov8n.pt")  # small model, replace with spine model later
GOOGLE_BOOKS_API = "https://www.googleapis.com/books/v1/volumes?q="

def detect_spines(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    results = model(img)
    cropped_spines = []

    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        crop = img[y1:y2, x1:x2]
        cropped_spines.append(crop)

    return cropped_spines

def extract_text(image):
    text = pytesseract.image_to_string(Image.fromarray(image))
    return text.strip()

def search_book(query):
    url = GOOGLE_BOOKS_API + query
    res = requests.get(url).json()

    if "items" not in res:
        return None

    info = res["items"][0]["volumeInfo"]
    return {
        "title": info.get("title", "Unknown"),
        "authors": info.get("authors", ["Unknown"]),
        "thumbnail": info.get("imageLinks", {}).get("thumbnail", "")
    }

def detect_books(image_bytes):
    spines = detect_spines(image_bytes)
    results = []

    for spine in spines:
        text = extract_text(spine)
        if len(text) < 3:
            continue
        book = search_book(text)
        if book:
            results.append(book)

    return results
