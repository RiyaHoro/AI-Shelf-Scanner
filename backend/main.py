from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, Book
from detect import detect_books

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/scan")
async def scan_books(image: UploadFile = File(...)):
    content = await image.read()

    books = detect_books(content)

    db = SessionLocal()

    # Save each book to DB (skip duplicates)
    for book in books:
        exists = db.query(Book).filter(Book.title == book["title"]).first()
        if not exists:
            new_book = Book(
                title=book["title"],
                authors=book["authors"],
                categories=book["categories"],
                rating=book["rating"],
                summary=book["summary"],
                thumbnail=book["thumbnail"]
            )
            db.add(new_book)
            db.commit()

    return {"books": books}


@app.get("/history")
def get_history():
    db = SessionLocal()
    rows = db.query(Book).order_by(Book.scanned_at.desc()).all()

    return [
        {
            "id": b.id,
            "title": b.title,
            "authors": b.authors,
            "categories": b.categories,
            "summary": b.summary,
            "rating": b.rating,
            "thumbnail": b.thumbnail,
            "scanned_at": b.scanned_at
        }
        for b in rows
    ]


@app.delete("/delete/{book_id}")
def delete_book(book_id: int):
    db = SessionLocal()
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        return {"error": "Not found"}

    db.delete(book)
    db.commit()

    return {"message": "Deleted"}
