from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_serializer, field_validator, validator
from datetime import datetime, timedelta
from typing import List, Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('created_at')
    def serialize_dt(self, dt: datetime, _info):
        return dt.isoformat()

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class BookBase(BaseModel):
    title: str
    author: str
    price: float

class BookCreate(BookBase):
    stock: int = 0

class Book(BookBase):
    id: int
    stock: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('created_at')
    def serialize_dt(self, dt: datetime, _info):
        return dt.isoformat()

class CartBase(BaseModel):
    book_id: int
    quantity: int = 1

class CartCreate(CartBase):
    pass

class Cart(CartBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('created_at')
    def serialize_dt(self, dt: datetime, _info):
        return dt.isoformat()

class CartCreate(BaseModel):
    book_id: int
    quantity: int = 1
    user_id: int

    @field_validator('quantity')
    def validate_quantity(cls, v):
        if v < 1:
            raise ValueError("Quantity must be at least 1")
        return v

class CartItemBase(BaseModel):
    book_id: int = Field(..., gt=0, description="ID книги должен быть положительным числом")
    quantity: int = Field(1, gt=0, le=100, description="Количество должно быть от 1 до 100")

    @validator('quantity')
    def validate_quantity(cls, v):
        if v < 1:
            raise ValueError("Количество не может быть меньше 1")
        return v

class CartItemCreate(CartItemBase):
    pass

class CartItem(CartItemBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class OrderBase(BaseModel):
    total: float
    status: str = "created"

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    user_id: int
    created_at: datetime
    items: List["OrderItem"] = []

    model_config = ConfigDict(from_attributes=True)

class OrderItemBase(BaseModel):
    book_id: int
    quantity: int
    price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    order_id: int

    model_config = ConfigDict(from_attributes=True)
