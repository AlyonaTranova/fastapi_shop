from sqlalchemy.orm import Session
from .. import models, schemas
from datetime import datetime

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(
        title=book.title,
        author=book.author,
        price=book.price,
        stock=book.stock,
        created_at=datetime.utcnow()
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()
