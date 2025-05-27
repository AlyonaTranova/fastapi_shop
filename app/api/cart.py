from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas
from ..crud import cart as crud_cart
from ..crud import users as crud_users

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/", response_model=schemas.Cart)
def add_to_cart(
    cart: schemas.CartCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    # Проверяем существование пользователя
    db_user = crud_users.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {user_id} not found"
        )

    # Проверяем существование книги (добавьте аналогичную проверку)
    # ...

    return crud_cart.add_to_cart(db=db, cart=cart, user_id=user_id)
