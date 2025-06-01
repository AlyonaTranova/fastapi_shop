from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models
from ..crud import cart as crud_cart
from ..crud import users as crud_users
from ..api.auth import get_current_user

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

@router.post(
    "/",
    response_model=schemas.CartItem,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"description": "Недостаточно товара на складе"},
        404: {"description": "Книга не найдена"}
    }
)
async def add_to_cart(
    item: schemas.CartItemCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    # Проверяем существование книги
    book = db.query(models.Book).filter(models.Book.id == item.book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена"
        )

    # Проверяем доступное количество
    if book.stock < item.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Доступно только {book.stock} шт. этого товара"
        )

    try:
        return crud_cart.add_to_cart(db, item, current_user.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/", response_model=schemas.CartItem)
def add_item_to_cart(
    cart_item: schemas.CartItemCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud_cart.add_to_cart(db, cart_item, current_user.id)

@router.get("/", response_model=list[schemas.CartItem])
def get_user_cart(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud_cart.get_cart_items(db, current_user.id)

@router.delete("/{item_id}")
def remove_item_from_cart(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    crud_cart.remove_from_cart(db, item_id, current_user.id)
    return {"message": "Item removed from cart"}
