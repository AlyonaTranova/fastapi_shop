# Экспорт модулей для удобного импорта
from .crud import auth as crud_auth
from .crud import books as crud_books
from .crud import cart as crud_cart
from .crud import users as crud_users

__all__ = [
    "crud_auth",
    "crud_books",
    "crud_cart",
    "crud_users"
]
