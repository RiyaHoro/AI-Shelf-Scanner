from sqlalchemy import create_engine, Column, Integer, Text, TIMESTAMP
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

# Local PostgreSQL
DATABASE_URL = "postgresql://ai_shelf_scannerdb_user:uCjC7z0RwZeZA5NHmYZeqUUKzxGgHKbU@dpg-d4l59nali9vc73e3ign0-a.oregon-postgres.render.com/ai_shelf_scannerdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text)
    authors = Column(Text)
    categories = Column(Text)
    rating = Column(Text)
    summary = Column(Text)
    thumbnail = Column(Text)
    scanned_at = Column(TIMESTAMP, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)
