from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.books import BooksModel
from app.schemas.books import BooksCreate, BooksUpdate
from app.repositories.books_repo import (
    fetch_all_books,
    fetch_books_by_id,
    fetch_books_by_title,
    fetch_books_author,
    books_create,
    books_update,
    books_delete
)

async def get_all_books(db: AsyncSession):
    return await fetch_all_books(db)

async def get_book_by_id(db: AsyncSession, book_id: str) -> BooksModel | None:
    book = await fetch_books_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return book

async def get_book_by_title(db: AsyncSession, book_title: str) -> BooksModel | None:
    book = await fetch_books_by_title(db, book_title)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

async def get_book_by_author(db: AsyncSession, author: str) -> BooksModel | None:
    book = await fetch_books_author(db, author)
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return book

async def add_book(db: AsyncSession, body: BooksCreate, user_id: str) -> BooksModel | None:
    
    if len(body.title) < 3:
        raise HTTPException(status_code=400, detail="book title must be at least 3 charaters")
    
    data = body.model_dump()
    data["user_id"] = user_id 

    return await books_create(db=db, data=data)

async def edit_book(db: AsyncSession, book_title:str , body: BooksUpdate) -> BooksModel | None:
    data = body.model_dump(exclude_unset=True)

    if not data:
        raise HTTPException(status_code=400, detail="Nothing to update")
    
    book = await fetch_books_by_title(db, book_title)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return await books_update(db, data, book_title)

async def remove_book(db: AsyncSession, book_title: str) -> dict | None:
    book = await fetch_books_by_title(db, book_title)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    await books_delete(db, book)
    return {"message": "Book deleted successfully"}

