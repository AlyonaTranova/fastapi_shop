from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy import URL, create_engine, text
from config import settings
import asyncio

async_engine = create_async_engine(url=settings.DATABASE_URL_asyncpg, echo=False)

async def get_1():
    async with async_engine.connect() as conn:
        query = "SELECT VERSION()"
        res = await conn.execute(text(query))
        print(f"{res.first()=}")

asyncio.run(get_1())