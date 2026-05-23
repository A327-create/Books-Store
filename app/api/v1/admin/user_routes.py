from fastapi import APIRouter, status, Depends
from app.services.admin.user_service import (
    update_user_profile, 
    admin_delete_user, 
    get_all_users
)
from app.dependencies.auth import get_admin_user
from app.dependencies.db import get_db
from app.models.user import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import (
    UserResponse, 
    AdminUserUpdate
)
router = APIRouter(prefix="/admin/user", tags=["adminuser"])

@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def all_users(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_admin_user)
):
    return await get_all_users(db, current_user)

@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def admin_update_user(
    user_id: str,
    body: AdminUserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_admin_user)
):
    return await update_user_profile(db, user_id, body)  

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def admin_delete(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_admin_user)
):
    return await admin_delete_user(db, user_id, current_user)

