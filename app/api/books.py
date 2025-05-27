from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas
from ..crud.books import create_book, get_books  # Импорт из crud/books.py

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=schemas.Book)
def create_book_route(
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
):
    return create_book(db=db, book=book)  # Вызов CRUD функции

@router.get("/", response_model=list[schemas.Book])
def read_books(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_books(db, skip=skip, limit=limit)
