# schemas.py
from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    title: str
    authors: str
    thumbnail: str
    summary: str
    categories: str
    rating: str

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    class Config:
        from_attributes = True
