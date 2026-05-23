from datetime import datetime
from typing import TypedDict
import re

def validate_password(password: str) -> bool:
    """
    Strong password check:
    - min 8 chars
    - 1 uppercase
    - 1 lowercase
    - 1 digit
    - 1 special char
    """
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(pattern, password) is not None

def password_error_message() -> str:
    return (
        "Password must be at least 8 characters long and include "
        "uppercase, lowercase, number, and special character"
    )

def generate_slug(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)   # ✅ multiple dashes fix
    return text.strip("-")

def format_datetime(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")

class Pagination(TypedDict):
    skip: int
    limit: int

def get_pagination(skip: int = 0, limit: int = 10) -> Pagination:
    return {"skip": skip, "limit": limit}

def mask_email(email: str) -> str:
    if "@" not in email:
        return email
    name, domain = email.split("@", 1)
    visible = name[0] if name else "*"
    return visible + "***@" + domain




