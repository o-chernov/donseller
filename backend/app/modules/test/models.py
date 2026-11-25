import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import String, false, func
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from app.core.database import Base


class UserStatus(StrEnum):
    ACTIVE = "active"
    BLOCKED = "blocked"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid7)
    email: Mapped[str] = mapped_column(String(320), unique=True)
    username: Mapped[str | None] = mapped_column(
        String(180), unique=True)
    password_hash: Mapped[str]
    is_email_verified: Mapped[bool] = mapped_column(server_default=false())
    status: Mapped[UserStatus] = mapped_column(default=UserStatus.ACTIVE)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
