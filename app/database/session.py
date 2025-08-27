from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from typing import Annotated
from app.config import db_settings as settings

# engine=create_engine(
#     "sqlite:///sqlite.db", echo=True, connect_args={"check_same_thread": False}
# )
engine = create_async_engine(url=settings.POSTGRES_URL, echo=True)


# def create_db_tables():
#     from app.schemas import Shipment

#     SQLModel.metadata.create_all(bind=engine)


async def create_db_tables():
    async with engine.begin() as conn:
        from .models import Shipment  # noqa: F401

        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async_session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
