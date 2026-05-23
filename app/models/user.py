from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.utils.enums import UserRole
from uuid import uuid4
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.refresh_token import RefreshTokenModel
    from app.models.books import BooksModel

class UserModel(Base):
    __tablename__ = "users"

    id:         Mapped[str]      = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    username:   Mapped[str]      = mapped_column(String(50), unique=True, index=True)
    email:      Mapped[str]      = mapped_column(String(255), unique=True, index=True)
    fullname:   Mapped[str]      = mapped_column(String(255), nullable=True)
    password:   Mapped[str]      = mapped_column(String(255))
    role:       Mapped[str]      = mapped_column(String(50), default=UserRole.USER)
    is_admin:   Mapped[bool]     = mapped_column(Boolean, default=False)
    is_active:  Mapped[bool]     = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    tokens: Mapped[list["RefreshTokenModel"]] = relationship(back_populates="user")
    books:  Mapped[list["BooksModel"]]        = relationship("BooksModel", back_populates="user")

   