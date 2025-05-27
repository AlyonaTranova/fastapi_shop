from fastapi import FastAPI
from .database import engine, Base
from .api import auth, books, cart, users

app = FastAPI()

# Подключение всех роутеров
app.include_router(auth.router)
app.include_router(books.router)
app.include_router(cart.router)
app.include_router(users.router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to Bookstore API"}
