from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.config import settings
from app.models.refresh_token import RefreshTokenModel
# from typing import Sequence
from datetime import datetime, timedelta

async def save_refresh_token(db: AsyncSession, token: str, user_id: str) -> None: 
    expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    new_token = RefreshTokenModel(token=token, user_id=user_id, expires_at=expires_at)
    db.add(new_token)
    await db.commit()

async def is_token_revoked(db: AsyncSession, token: str) -> bool:
    result = await db.execute(select(RefreshTokenModel).where(RefreshTokenModel.token == token))
    existing = result.scalar_one_or_none()
    return existing is None or existing.is_revoked

async def revoke_refresh_token(db: AsyncSession, token: str) -> bool:
    result = await db.execute(
        select(RefreshTokenModel).where(RefreshTokenModel.token == token)
    )
    existing = result.scalar_one_or_none()

    if not existing or existing.is_revoked:
        return False

    existing.is_revoked = True
    await db.commit()
    return True