from pydantic import BaseModel, ConfigDict, EmailStr, field_serializer, GetCoreSchemaHandler
from pydantic_core import core_schema
from datetime import datetime
from typing import Any, Optional

# Кастомный тип DateTime для обработки datetime
class DateTime(datetime):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.datetime_schema()

# Хелперы для конвертации
def convert_to_datetime(dt: datetime) -> DateTime:
    return DateTime(
        dt.year, dt.month, dt.day,
        dt.hour, dt.minute, dt.second,
        dt.microsecond, dt.tzinfo
    )

# User Models
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: DateTime
    updated_at: DateTime

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('created_at', 'updated_at')
    def serialize_dt(self, dt: DateTime, _info):
        return dt.isoformat()

# Book Models
class BookBase(BaseModel):
    title: str
    author: str
    price: float

class BookCreate(BookBase):
    description: Optional[str] = None
    stock: int = 0

class Book(BookBase):
    id: int
    description: Optional[str] = None
    stock: int
    created_at: DateTime

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('created_at')
    def serialize_dt(self, dt: DateTime, _info):
        return dt.isoformat()

# Cart Models
class CartBase(BaseModel):
    book_id: int
    quantity: int = 1

class CartCreate(CartBase):
    pass

class Cart(CartBase):
    id: int
    user_id: int
    created_at: DateTime

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('created_at')
    def serialize_dt(self, dt: DateTime, _info):
        return dt.isoformat()

# Order Models
class OrderBase(BaseModel):
    total: float
    status: str = "created"

class OrderCreate(OrderBase):
    shipping_address: str
    payment_method: str

class Order(OrderBase):
    id: int
    user_id: int
    created_at: DateTime

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('created_at')
    def serialize_dt(self, dt: DateTime, _info):
        return dt.isoformat()
