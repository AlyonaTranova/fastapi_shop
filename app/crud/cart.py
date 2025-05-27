from sqlalchemy.orm import Session
from .. import models, schemas
from datetime import datetime

def add_to_cart(db: Session, cart: schemas.CartCreate, user_id: int):
    db_cart = models.Cart(
        **cart.model_dump(),
        user_id=user_id,
        created_at=datetime.utcnow()
    )
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

def get_user_cart(db: Session, user_id: int):
    return db.query(models.Cart).filter(models.Cart.user_id == user_id).all()
