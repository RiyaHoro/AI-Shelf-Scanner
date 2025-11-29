import cv2
import pytesseract
import io
import requests
from PIL import Image
from ultralytics import YOLO
import numpy as np

model = YOLO("yolov8n.pt")

GOOGLE_BOOKS_API = "https://www.googleapis.com/books/v1/volumes?q="

def detect_spines(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, (640, 640))

    results = model(img)
    cropped = []

    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        crop = img[y1:y2, x1:x2]
        cropped.append(crop)

    return cropped


def extract_text(image):
    text = pytesseract.image_to_string(Image.fromarray(image))
    return text.strip()


def fetch_book_details(query):
    res = requests.get(GOOGLE_BOOKS_API + query).json()

    if "items" not in res:
        return None

    info = res["items"][0]["volumeInfo"]

    return {
        "title": info.get("title", "Unknown"),
        "authors": ", ".join(info.get("authors", ["Unknown"])),
        "thumbnail": info.get("imageLinks", {}).get("thumbnail", ""),
        "summary": info.get("description", "No summary available"),
        "categories": ", ".join(info.get("categories", ["Uncategorized"])),
        "rating": str(info.get("averageRating", "N/A"))
    }


def detect_books(image_bytes):
    spines = detect_spines(image_bytes)
    detected = []

    for spine in spines:
        text = extract_text(spine)

        if len(text) < 3:
            continue

        book = fetch_book_details(text)

        if book:
            detected.append(book)

    return detected
