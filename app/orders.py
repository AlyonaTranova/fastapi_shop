from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import schemas, crud
from .database import get_db
from .core.security import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=schemas.Order)
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.create_order(db=db, order=order, user_id=current_user.id)
