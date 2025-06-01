from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas
from ..crud import orders as crud_orders
from ..api.auth import get_current_user
from .. import models

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=schemas.Order)
def create_new_order(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud_orders.create_order(db, current_user.id)

@router.get("/", response_model=list[schemas.Order])
def get_user_orders(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return db.query(models.Order).filter(models.Order.user_id == current_user.id).all()
