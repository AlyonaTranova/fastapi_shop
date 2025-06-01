from sqlalchemy.orm import Session
from .. import models, schemas
from datetime import datetime
from sqlalchemy.exc import IntegrityError

def add_to_cart(db: Session, cart_item: schemas.CartItemCreate, user_id: int):
    # Проверяем, есть ли уже такой товар в корзине
    existing_item = db.query(models.CartItem).filter(
        models.CartItem.user_id == user_id,
        models.CartItem.book_id == cart_item.book_id
    ).first()

    if existing_item:
        # Обновляем количество, если товар уже в корзине
        existing_item.quantity += cart_item.quantity
    else:
        # Создаем новую запись
        existing_item = models.CartItem(
            **cart_item.model_dump(),
            user_id=user_id,
            created_at=datetime.utcnow()
        )
        db.add(existing_item)

    db.commit()
    db.refresh(existing_item)
    return existing_item

def get_user_cart(db: Session, user_id: int):
    return db.query(models.Cart).filter(models.Cart.user_id == user_id).all()

def get_cart_items(db: Session, user_id: int):
    return db.query(models.CartItem).filter(models.CartItem.user_id == user_id).all()


def remove_from_cart(db: Session, cart_item_id: int, user_id: int):
    db.query(models.CartItem).filter(
        models.CartItem.id == cart_item_id,
        models.CartItem.user_id == user_id
    ).delete()
    db.commit()
