from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.db import get_db
from app.schemas.user import (
    UserCreate, 
    UserLogin, 
    LogoutRequest
)
from app.schemas.refresh_token import Token, RefreshTokenSchema
from app.services.auth_service import (
    user_registor,
    login_user,
    refresh_access_token,
    logout_user
)
from app.dependencies.auth import (
    get_current_user,
)

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
    body: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    return await user_registor(db=db, body=body)

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(
    body: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    return await login_user(db, body)

@router.post("/refresh", response_model=Token, status_code=status.HTTP_200_OK)
async def refresh_token(
    body: RefreshTokenSchema, 
    db: AsyncSession = Depends(get_db)
):
    return await refresh_access_token(db, body.refresh_token)

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    data: LogoutRequest, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await logout_user(db, data.refresh_token)
