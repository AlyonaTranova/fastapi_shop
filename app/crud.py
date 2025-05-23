from datetime import datetime
from sqlalchemy.orm import Session
from . import models
from . import schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(
        title=book.title,
        author=book.author,
        price=book.price,
        description=book.description,
        stock=book.stock,
        created_at=datetime.utcnow()  # Автоматическое заполнение
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book  # SQLAlchemy автоматически заполнит id

def add_to_cart(db: Session, cart_item: schemas.CartCreate, user_id: int):
    db_cart = models.Cart(**cart_item.model_dump(), user_id=user_id)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

def create_order(db: Session, order: schemas.OrderCreate, user_id: int):
    db_order = models.Order(**order.model_dump(), user_id=user_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def add_order_item(db: Session, item: schemas.OrderItemCreate, order_id: int):
    db_item = models.OrderItem(**item.model_dump(), order_id=order_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_user_cart(db: Session, user_id: int):
    return db.query(models.Cart).filter(models.Cart.user_id == user_id).all()
