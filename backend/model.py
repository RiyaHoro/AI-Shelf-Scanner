# models.py
from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from database import Base

class BookScan(Base):
    __tablename__ = "book_scans"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    authors = Column(String)
    thumbnail = Column(String)
    summary = Column(String)
    categories = Column(String)
    rating = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
