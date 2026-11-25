import enum
from collections.abc import AsyncGenerator
from datetime import datetime
from typing import Annotated

from fastapi import Depends
from sqlalchemy import DateTime, Enum, MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.settings import settings


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )
    type_annotation_map = {
        datetime: DateTime(timezone=True),
        enum.Enum: Enum(
            enum.Enum,
            native_enum=False,
            length=None,
            validate_strings=True,
            values_callable=lambda members: [
                member.value for member in members],
        ),
    }
    __mapper_args__ = {"eager_defaults": True}


# Небольшой пул: не больше 10 подключений (5 постоянных + 5 временных),
# у роли базы на сервере лимит 40. pool_pre_ping проверяет подключение
# перед выдачей: база перезапускается при еженедельном обновлении.
engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=5,
)
session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with session_factory() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db)]
