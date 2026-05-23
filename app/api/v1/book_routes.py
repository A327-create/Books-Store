from fastapi import status, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.db import get_db
from app.models.books import BooksModel
from app.models.user import UserModel
from app.schemas.books import (
    BooksCreate,
    BooksResponse,
    BooksUpdate,
)
from app.dependencies.auth import (
    get_current_user
)
from app.services.book_service import (
    get_all_books,
    get_book_by_id,
    get_book_by_title,
    get_book_by_author,
    add_book,
    edit_book,
    remove_book
)
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

router = APIRouter(prefix="/book", tags=["Book"])

@router.get("/", response_model=Page[BooksResponse], status_code=status.HTTP_200_OK)
async def all_books(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    query = await get_all_books(db)
    return await paginate(db, query)

@router.get('/title/{book_title}', response_model=BooksResponse, status_code=status.HTTP_200_OK)
async def book_by_title(
    book_title: str,
    db: AsyncSession = Depends(get_db),
    current_user:  UserModel = Depends(get_current_user)
):
    query = await get_book_by_title(db, book_title)
    return query

@router.get('/id/{book_id}', response_model=BooksResponse, status_code=status.HTTP_200_OK)
async def book_by_id(
    book_id: str,
    db: AsyncSession = Depends(get_db),
    current_user:  UserModel = Depends(get_current_user)
):
    query = await get_book_by_id(db, book_id)
    return query

@router.get('author/{author}', response_model=BooksResponse, status_code=status.HTTP_200_OK)
async def book_by_author(
    author: str,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> BooksModel | None:
    query = await get_book_by_author(db, author)
    return query

@router.post('/', response_model=BooksResponse, status_code=status.HTTP_201_CREATED)
async def create(
    body: BooksCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
) -> BooksModel | None:
    query = await add_book(db, body, current_user.id)
    return query

@router.patch('/{book_title}', response_model=BooksResponse, status_code=status.HTTP_200_OK)
async def update(
    book_title: str,
    body: BooksUpdate,
    db: AsyncSession = Depends(get_db), 
    current_user: UserModel = Depends(get_current_user)
) -> BooksModel | None:

    query = await edit_book(db, book_title, body)
    return query

@router.delete('/{book_title}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    book_title: str,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)    
):
    await remove_book(db, book_title)
