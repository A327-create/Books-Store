from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.models.user import UserModel
from app.services.user_service import (
    update_me,
    delete_me,
)
from app.schemas.user import (
    UserUpdate,
    UserPublicResponse
)

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/me", response_model=UserPublicResponse)
async def me(
    current_user: UserModel = Depends(get_current_user)
):
    return current_user

@router.patch("/me", response_model=UserPublicResponse, status_code=status.HTTP_201_CREATED)
async def update(
    body: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return await update_me(db, current_user.id, body)

@router.delete("/me", status_code=status.HTTP_200_OK)
async def delete(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return await delete_me(db, user_id)


