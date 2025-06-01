from sqlalchemy.orm import Session
from .. import models, schemas
from datetime import datetime
from .cart import get_cart_items

def create_order(db: Session, user_id: int):
    # Получаем товары из корзины
    cart_items = get_cart_items(db, user_id)

    # Рассчитываем общую сумму
    total = sum(item.book.price * item.quantity for item in cart_items)

    # Создаем заказ
    db_order = models.Order(
        user_id=user_id,
        total=total,
        created_at=datetime.utcnow()
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Добавляем товары в заказ
    for item in cart_items:
        db_item = models.OrderItem(
            order_id=db_order.id,
            book_id=item.book_id,
            quantity=item.quantity,
            price=item.book.price
        )
        db.add(db_item)

    # Очищаем корзину
    db.query(models.CartItem).filter(models.CartItem.user_id == user_id).delete()

    db.commit()
    return db_order
