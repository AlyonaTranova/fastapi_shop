from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import schemas, crud
from .database import get_db

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/", response_model=schemas.Cart)
def add_to_cart(
    cart_item: schemas.CartCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    return crud.add_to_cart(db, cart_item, user_id)
