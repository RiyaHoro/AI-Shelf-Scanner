from fastapi import FastAPI, UploadFile, File
from detect import detect_books
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, timeout_keep_alive=120)



@app.post("/scan")
async def scan_books(image: UploadFile = File(...)):
    img_bytes = await image.read()
    result = detect_books(img_bytes)
    return {"books": result}
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-shelf-scanner.vercel.app",
        "http://localhost:5173",
        "*"
     ],
 # Allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

