from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models.user import UserModel
from app.schemas.user import UserUpdate
from app.repositories.user_repo import (
    user_delete,
    fetch_user_by_id,
    user_update
)
async def update_me(db: AsyncSession, user_id: str, body: UserUpdate) -> UserModel | None:
    data = body.model_dump(exclude_unset=True)

    if not data:
        raise HTTPException(status_code=400, detail="Nothing to update")
    user = await fetch_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return await user_update(db, data, user_id)

async def delete_me(db: AsyncSession, user_id: str) -> dict:
    user = await fetch_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await user_delete(db, user)
    return {"message": "Account deleted successfully"}


