from fastapi import FastAPI, UploadFile, File
from detect import detect_books
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.post("/scan")
async def scan_books(image: UploadFile = File(...)):
    img_bytes = await image.read()
    result = detect_books(img_bytes)
    return {"books": result}
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
