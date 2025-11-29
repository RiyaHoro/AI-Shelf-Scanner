# crud.py
from sqlalchemy.orm import Session
from models import BookScan
from schemas import BookCreate

def save_book(db: Session, data: BookCreate):
    book = BookScan(
        title=data.title,
        authors=data.authors,
        thumbnail=data.thumbnail,
        summary=data.summary,
        categories=data.categories,
        rating=data.rating
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_scan_history(db: Session, limit: int = 20):
    return db.query(BookScan).order_by(BookScan.id.desc()).limit(limit).all()
