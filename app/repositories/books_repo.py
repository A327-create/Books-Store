from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.books import BooksModel

async def fetch_all_books(db: AsyncSession):
    return select(BooksModel)

async def fetch_books_by_id(db: AsyncSession, book_id: str) -> BooksModel | None:
    result = await db.execute(select(BooksModel).where(BooksModel.id == book_id))
    book = result.scalar_one_or_none()
    return book

async def fetch_books_by_title(db: AsyncSession, book_title: str) -> BooksModel | None:
    result = await db.execute(select(BooksModel).where(BooksModel.title == book_title))
    book = result.scalars().first()
    return book

async def fetch_books_author(db: AsyncSession, author: str) -> BooksModel | None:
    result = await db.execute(select(BooksModel).where(BooksModel.author == author))
    book = result.scalars().first()
    return book

async def books_create(db: AsyncSession, data: dict) -> BooksModel | None:
    new_book = BooksModel(**data)
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book

async def books_update(db: AsyncSession, data:dict, book_title:str) -> BooksModel | None:
    result = await db.execute(select(BooksModel).where(BooksModel.title == book_title))
    book = result.scalar_one_or_none()

    if not book:
        return None

    for key, value in data.items():
        setattr(book, key, value)


    await db.commit()
    await db.refresh(book)
    return book

async def books_delete(db: AsyncSession, book: BooksModel) -> None:
    await db.delete(book)
    await db.commit()
