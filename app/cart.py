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

@router.post("/checkout/", response_model=schemas.Order)
def checkout_cart(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    # 1. Получаем товары из корзины
    cart_items = crud.get_user_cart(db, user_id=current_user.id)

    # 2. Создаем заказ
    total = sum(item.book.price * item.quantity for item in cart_items)
    order = crud.create_order(db, schemas.OrderCreate(total=total), current_user.id)

    # 3. Переносим товары в заказ
    for item in cart_items:
        crud.add_order_item(
            db,
            schemas.OrderItemCreate(
                book_id=item.book_id,
                quantity=item.quantity,
                price=item.book.price
            ),
            order.id
        )
        # Удаляем из корзины
        db.delete(item)

    db.commit()
    return order
