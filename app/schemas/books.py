from pydantic import BaseModel
from datetime import datetime

class BooksCreate(BaseModel):
    title: str
    author: str
    price: float
    isbn: str
    published_date: datetime

class BooksResponse(BaseModel):
    title: str
    author: str
    price: float
    isbn: str
    published_date: datetime
    created_at: datetime

class BooksUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    price: float | None = None
    isbn: str | None = None
    published_date: datetime | None = None

