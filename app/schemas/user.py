from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    fullname: str | None = None

    model_config = {"from_attributes": True}

class UserResponse(BaseModel):
    username: str
    email: str
    fullname: str
    is_active: bool
    is_admin: bool
    craeted_at: datetime

    model_config = {"from_attributes": True}

class UserLogin(BaseModel):
    identifier: str
    password: str

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    username: Optional[str]
    fullname: Optional[str]
    email: Optional[str]

    model_config = {"from_attributes": True}

class UserPublicResponse(BaseModel):
    username: str
    email: str
    fullname: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}

class AdminUserUpdate(BaseModel):
    fullname: str
    is_admin: bool | None = None
    is_active: bool | None = None

    model_config = {"from_attributes": True}

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

    model_config = {"from_attributes": True}

class AuthResponse(BaseModel):
    user: UserPublicResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearar"

    model_config = {"from_attributes": True}

class LogoutRequest(BaseModel):
    refresh_token: str

    model_config = {"from_attributes": True}
