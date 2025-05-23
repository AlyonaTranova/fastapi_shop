from pydantic import BaseModel, EmailStr, ConfigDict, field_serializer
import datetime
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema
from datetime import datetime
from typing import Any, Optional

class DateTime(datetime):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.datetime_schema()

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,  # Ранее orm_mode=True
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )

class BookBase(BaseModel):
    title: str
    author: str
    price: float

class BookCreate(BookBase):
    description: Optional[str] = None
    stock: Optional[int] = 0

class Book(BookBase):
    id: int
    description: Optional[str] = None
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

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )


class OrderBase(BaseModel):
    user_id: int
    total: float
    status: str = "created"

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    created_at: datetime

    # Новый стиль конфигурации Pydantic v2
    model_config = ConfigDict(
        from_attributes=True,  # Аналог старого orm_mode=True
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )

    # Сериализатор для datetime (альтернатива json_encoders)
    @field_serializer('created_at')
    def serialize_dt(self, dt: datetime, _info):
        return dt.isoformat()

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
