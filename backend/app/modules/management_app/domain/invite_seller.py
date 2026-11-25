# Приглошение -- Это бизнес правило, оно находится в самом внутреннем круге. В этом файле не должно быть зависимостей от внешних кругов(Тут нельзя вызывать методы и классы из нижних иерархий).

# class Invitation
# Для приглошение в данный момент нужно имя и роль: management, seller, shopper

import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import String, false, func
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from backend.app.core.db import Base


class InviteSellerStatus(StrEnum):
    APPROVED = "approved"
    WAITING = "watting"


class InviteSeller(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid7)
    point_name: Mapped[str] = mapped_column(String(320), unique=True)
    city: Mapped[str] = mapped_column(String(320))
    status: Mapped[UserStatus] = mapped_column(default=UserStatus.ACTIVE)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
