import cv2
import pytesseract
import numpy as np
import requests
import io
from PIL import Image, ImageEnhance

# Load EAST model (VERY lightweight ~2MB)
EAST_MODEL_PATH = "frozen_east_text_detection.pb"

GOOGLE_BOOKS_API = "https://www.googleapis.com/books/v1/volumes?q="


# ============================
# 🔥 IMAGE PREPROCESSING
# ============================
def preprocess_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # Increase clarity for OCR
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.7)

    # Convert to OpenCV format
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Resize for EAST
    orig = img.copy()
    h, w = img.shape[:2]
    new_w, new_h = (320, 320)
    rW = w / float(new_w)
    rH = h / float(new_h)

    img = cv2.resize(img, (new_w, new_h))
    blob = cv2.dnn.blobFromImage(
        img, 1.0, (new_w, new_h),
        (123.68, 116.78, 103.94), swapRB=True, crop=False
    )

    return blob, orig, rW, rH


# ============================
# 🔥 EAST TEXT DETECTION
# ============================
def detect_text_regions(image_bytes):
    blob, orig, rW, rH = preprocess_image(image_bytes)

    net = cv2.dnn.readNet(EAST_MODEL_PATH)
    net.setInput(blob)

    # EAST output layers
    scores, geometry = net.forward([
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"
    ])

    rects = []
    confidences = []

    h, w = scores.shape[2:4]

    # Decode EAST scores & geometry
    for y in range(0, h):
        scores_data = scores[0, 0, y]
        x0 = geometry[0, 0, y]
        x1 = geometry[0, 1, y]
        x2 = geometry[0, 2, y]
        x3 = geometry[0, 3, y]
        angles = geometry[0, 4, y]

        for x in range(0, w):
            if scores_data[x] < 0.5:  # threshold
                continue

            angle = angles[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            h_val = x0[x] + x2[x]
            w_val = x1[x] + x3[x]

            end_x = int(x * 4 + cos * w_val + sin * h_val)
            end_y = int(y * 4 - sin * w_val + cos * h_val)
            start_x = int(x * 4)
            start_y = int(y * 4)

            rects.append((start_x, start_y, end_x, end_y))
            confidences.append(float(scores_data[x]))

    # Non-max suppression (remove overlapping boxes)
    boxes = cv2.dnn.NMSBoxes(
        rects, confidences,
        score_threshold=0.5,
        nms_threshold=0.4
    )

    final_boxes = []
    if len(boxes) > 0:
        for i in boxes.flatten():
            start_x, start_y, end_x, end_y = rects[i]

            # Scale back to original image size
            start_x = int(start_x * rW)
            start_y = int(start_y * rH)
            end_x = int(end_x * rW)
            end_y = int(end_y * rH)

            final_boxes.append((start_x, start_y, end_x, end_y))

    return final_boxes, orig


# ============================
# 🔥 OCR -- Extract Text
# ============================
def extract_text(img_region):
    gray = cv2.cvtColor(img_region, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 1)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)[1]

    text = pytesseract.image_to_string(gray, config="--psm 6")
    text = text.strip()

    # Clean output
    text = "".join(c for c in text if c.isalnum() or c.isspace())
    return text


# ============================
# 🔥 GOOGLE BOOKS SEARCH (+best match)
# ============================
def fetch_book_details(query):
    if not query or len(query) < 3:
        return None

    url = GOOGLE_BOOKS_API + query.replace(" ", "+")
    try:
        raw = requests.get(url, timeout=5).json()
    except:
        return None

    if "items" not in raw:
        return None

    # Choose best match (highest similarity)
    best = raw["items"][0]["volumeInfo"]

    return {
        "title": best.get("title", "Unknown"),
        "authors": best.get("authors", ["Unknown"]),
        "thumbnail": best.get("imageLinks", {}).get("thumbnail", ""),
        "summary": best.get("description", "No summary available"),
        "categories": best.get("categories", ["Uncategorized"]),
        "rating": best.get("averageRating", "N/A"),
    }


# ============================
# 🔥 MASTER PIPELINE
# ============================
def detect_books(image_bytes):
    boxes, orig = detect_text_regions(image_bytes)

    results = []
    used_queries = set()

    for (x1, y1, x2, y2) in boxes[:12]:  # read top 12 text regions
        region = orig[y1:y2, x1:x2]

        text = extract_text(region)
        if not text or text in used_queries:
            continue

        used_queries.add(text)

        book = fetch_book_details(text)
        if book:
            results.append(book)

    return results
