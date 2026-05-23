from sqlalchemy import String, Text, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from datetime import datetime
from uuid import uuid4
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import UserModel

class RefreshTokenModel(Base):
    __tablename__ = "refresh_tokens"

    id:         Mapped[str]      = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    token:      Mapped[str]      = mapped_column(Text, unique=True, index=True)
    user_id:    Mapped[str]      = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    is_revoked: Mapped[bool]     = mapped_column(Boolean, default=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["UserModel"] = relationship(back_populates="tokens")


