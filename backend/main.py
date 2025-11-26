from fastapi import FastAPI, UploadFile, File
from detect import detect_books

app = FastAPI()

@app.post("/scan")
async def scan_books(image: UploadFile = File(...)):
    img_bytes = await image.read()
    result = detect_books(img_bytes)
    return {"books": result}
