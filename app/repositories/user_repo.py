from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import UserModel
from sqlalchemy import select
from typing import Sequence

async def fetch_all_users(db: AsyncSession) -> Sequence[UserModel] | None:
    result = await db.execute(select(UserModel))
    user = result.scalars().all()
    return user

async def fetch_user_by_id(db: AsyncSession, user_id: str) -> UserModel | None:
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalar_one_or_none()
    return user

async def fetch_user_by_email(db: AsyncSession, email: str) -> UserModel | None:
    result = await db.execute(select(UserModel).where(UserModel.email == email))
    user = result.scalar_one_or_none()
    return user
async def fetch_user_by_username(db: AsyncSession, username: str) -> UserModel | None:
    result = await db.execute(select(UserModel).where(UserModel.username == username))
    user = result.scalar_one_or_none()
    return user

async def user_create(db: AsyncSession, data: dict)-> UserModel:
    new_user = UserModel(**data)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def user_update(db: AsyncSession, data: dict, user_id: str)-> UserModel | None:
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return None

    for key, value in data.items():
        setattr(user, key, value)
    
    await db.commit()
    await db.refresh(user)
    return user

async def user_delete(db: AsyncSession, user: UserModel) -> None:
    await db.delete(user)
    await db.commit()

async def update_user_by_admin(db: AsyncSession, data: dict, user_id: str) -> UserModel | None:
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return user

    for key, value in data.items():
        setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return user


