from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import UserModel
from app.schemas.user import AdminUserUpdate
from app.repositories.user_repo import (
    fetch_user_by_email, 
    fetch_user_by_id, 
    fetch_user_by_username,
    fetch_all_users,
    update_user_by_admin,
    user_delete

)
from typing import Sequence

async def get_all_users(db: AsyncSession, current_user: UserModel) -> Sequence[UserModel] | None:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access forbidden")
    return await fetch_all_users(db)

async def get_user_email(db: AsyncSession, email: str) -> UserModel:
    user = await fetch_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def get_user_id(db: AsyncSession, user_id: str) -> UserModel:
    user = await fetch_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def get_user_username(db: AsyncSession, username: str) -> UserModel:
    user = await fetch_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def update_user_profile(db: AsyncSession, user_id: str, body: AdminUserUpdate) -> UserModel | None:
    data = body.model_dump(exclude_unset=True)

    if not data:
        raise HTTPException(status_code=400, detail="Nothing to update")

    user = await fetch_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return await update_user_by_admin(db, data, user_id)

async def admin_delete_user(db: AsyncSession, user_id: str, current_user: UserModel) -> dict:

    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="Admin cannot delete admin")

    user = await fetch_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await user_delete(db, user)
    return {"message": f"User {user.username} deleted successfully"}


