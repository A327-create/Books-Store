from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repositories.user_repo import (
    fetch_user_by_id,
    fetch_user_by_email,
    fetch_user_by_username,
    user_create,
)
from app.core.security import (
    generate_auth_tokens,
    hash_password,
    verify_password,
    verify_token,
    create_access_token,
)
from app.core.config import settings
from datetime import timedelta

from app.schemas.user import (
    UserCreate,
    UserLogin
)
from app.repositories.refresth_token import (
    is_token_revoked,
    revoke_refresh_token
)
from app.utils.validators import (
    validate_password,  
    password_error_message, 
)

async def user_registor(db: AsyncSession, body: UserCreate):

    if len(body.username) < 3:
        raise HTTPException(status_code=400, detail="Username must be at least 3 characters")
    
    if validate_password(body.password):
        raise HTTPException(status_code=400, detail=password_error_message)
    
    if await fetch_user_by_email(db=db, email=body.email):
        raise HTTPException(status_code=400, detail="This email is already")
    
    if await fetch_user_by_username(db, username=body.username):
        raise HTTPException(status_code=400, detail="This username is alraedy exist")
    
    hashed_password = hash_password(body.password)
    
    data = body.model_dump()
    data["password"] = hashed_password

    user = await user_create(db=db, data=data)
    return await generate_auth_tokens(db, user)

async def login_user(db: AsyncSession, body: UserLogin):

    if '@' in body.identifier:
        user = await fetch_user_by_email(db, body.identifier)
    else:
        user = await fetch_user_by_username(db, body.identifier)
    
    if not user:
        raise HTTPException(status_code=404, detail="This username is not find")
    
    if not verify_password(body.password, user.password):
        raise HTTPException(status_code=404, detail=password_error_message())
    
    return await generate_auth_tokens(db, user)

async def refresh_access_token(db: AsyncSession, refresh_token: str):

    # 1. Revoked check
    if await is_token_revoked(db, refresh_token):
        raise HTTPException(status_code=401, detail="Token has been revoked")

    # 2. Verify token
    payload = verify_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # 3. Type check
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    # 4. User exist karta hai?
    user = await fetch_user_by_id(db, str(payload.get("sub")))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 5. Naya access token
    new_access_token = create_access_token(
        {
            "sub": payload.get("sub"),
            "email": payload.get("email"),
            "is_admin": payload.get("is_admin"),
            "type": "access",
        },
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"access_token": new_access_token, "token_type": "bearer"}


async def logout_user(db: AsyncSession, refresh_token: str):

    payload = verify_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    revoked = await revoke_refresh_token(db, refresh_token)
    if not revoked:
        raise HTTPException(status_code=400, detail="Already logged out")

    return {"message": "Logged out successfully"}