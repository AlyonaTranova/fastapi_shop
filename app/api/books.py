from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from ..database import get_db
from ... import models, schemas
from ..crud import (
    get_book,
    get_books,
    create_book,
    update_book,
    delete_book
)
from ..schemas import DateTime

router = APIRouter(prefix="/books", tags=["books"])

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas
from ..crud import create_book

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=schemas.Book)
def create_book_endpoint(
    book: schemas.BookCreate,  # Используем схему создания
    db: Session = Depends(get_db)
):
    return create_book(db=db, book=book)

@router.get("/{book_id}", response_model=schemas.Book)
def read_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    db_book = get_book(db, book_id=book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return db_book

@router.put("/{book_id}", response_model=schemas.Book)
def update_existing_book(
    book_id: int,
    book: schemas.BookCreate,  # Используем схему для обновления
    db: Session = Depends(get_db)
):
    db_book = update_book(db, book_id=book_id, book=book)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return db_book

@router.delete("/{book_id}")
def delete_existing_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    delete_book(db, book_id=book_id)
    return {"message": "Book deleted successfully"}
