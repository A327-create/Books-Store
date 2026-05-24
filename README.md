Bookstore REST API
A production-ready RESTful API for managing a bookstore, built with FastAPI, PostgreSQL (Supabase), and SQLAlchemy (async). The API supports full CRUD operations, JWT-based authentication with refresh tokens, role-based access control, and pagination.
---
Tech Stack
Layer	Technology
Framework	FastAPI
Database	PostgreSQL (Supabase)
ORM	SQLAlchemy (async)
DB Driver	asyncpg
Migrations	Alembic
Authentication	JWT (PyJWT) + Refresh Tokens
Password Hashing	pwdlib (Argon2)
Pagination	fastapi-pagination
Validation	Pydantic v2
Server	Uvicorn
---
Project Structure
```
bookstore-api/
├── app/
│   ├── main.py                  # App entry point, routers registered here
│   ├── core/
│   │   ├── config.py            # Environment settings (Pydantic BaseSettings)
│   │   ├── database.py          # Async SQLAlchemy engine & session
│   │   └── security.py          # Password hashing, token utilities
│   ├── models/
│   │   ├── user.py              # User SQLAlchemy table model
│   │   ├── books.py             # Book SQLAlchemy table model
│   │   └── refresh_token.py     # RefreshToken SQLAlchemy table model
│   ├── schemas/
│   │   ├── user.py              # Pydantic schemas for User
│   │   └── books.py             # Pydantic schemas for Books
│   ├── repositories/
│   │   ├── user_repo.py         # Raw DB queries for users
│   │   └── books_repo.py        # Raw DB queries for books
│   ├── services/
│   │   ├── auth_service.py      # Register, login, refresh token logic
│   │   ├── user_service.py      # User profile update/delete logic
│   │   ├── book_service.py      # Book CRUD business logic
│   │   └── admin/
│   │       └── user.py          # Admin user management logic
│   ├── api/
│   │   └── v1/
│   │       ├── auth_routes.py   # /auth endpoints
│   │       ├── user_routes.py   # /user endpoints
│   │       ├── book_routes.py   # /book endpoints
│   │       └── admin/
│   │           └── user_routes.py # /admin/user endpoints
│   ├── dependencies/
│   │   ├── auth.py              # get_current_user, get_admin_user
│   │   └── db.py                # get_db session dependency
│   └── utils/
│       └── enums.py             # UserRole enum
├── alembic/                     # Database migrations
├── requirements.txt
├── .env                         # Secret environment variables (not in git)
├── .env.example                 # Template for environment variables
└── README.md
```
---
Setup & Run Locally
1. Clone the repo
```bash
git clone <your-repo-url>
cd bookstore-api
```
2. Create virtual environment
```bash
python -m venv myvenv
myvenv\Scripts\activate        # Windows
source myvenv/bin/activate     # Mac/Linux
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Setup environment variables
```bash
cp .env.example .env
# Edit .env with your Supabase DATABASE_URL and SECRET_KEY
```
5. Run migrations
```bash
alembic upgrade head
```
6. Start the server
```bash
uvicorn app.main:app --reload
```
7. Open API docs
```
http://localhost:8000/api/docs
```
---
Environment Variables
```bash
DATABASE_URL=postgresql+asyncpg://user:password@host:port/dbname
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
APP_NAME=Bookstore API
```
---
API Endpoints
Auth (Public)
Method	Endpoint	Description
POST	`/api/v1/auth/register`	Register new user
POST	`/api/v1/auth/login`	Login & get tokens
POST	`/api/v1/auth/refresh`	Refresh access token
POST	`/api/v1/auth/logout`	Logout & revoke refresh token
User (Protected)
Method	Endpoint	Description
GET	`/api/v1/user/me`	Get current user profile
PATCH	`/api/v1/user/me`	Update current user profile
DELETE	`/api/v1/user/me`	Delete current user account
Books (GET public, rest protected)
Method	Endpoint	Description
GET	`/api/v1/book/`	Get all books (pagination + search)
GET	`/api/v1/book/id/{book_id}`	Get book by ID
GET	`/api/v1/book/author/{author}`	Get book by author
POST	`/api/v1/book/`	Add new book
PATCH	`/api/v1/book/{book_id}`	Update book
DELETE	`/api/v1/book/{book_id}`	Delete book
Admin (Admin only)
Method	Endpoint	Description
GET	`/api/v1/admin/user/`	Get all users
PATCH	`/api/v1/admin/user/{user_id}`	Update any user
DELETE	`/api/v1/admin/user/{user_id}`	Delete any user
---
Sample Requests
Register
```json
POST /api/v1/auth/register
{
    "username": "john_doe",
    "email": "john@example.com",
    "fullname": "John Doe",
    "password": "strongpassword123"
}
```
Login
```json
POST /api/v1/auth/login
{
    "email": "john@example.com",
    "password": "strongpassword123"
}
```
Add Book (Token required)
```
Authorization: Bearer <your_access_token>
```
```json
POST /api/v1/book/
{
    "title": "Atomic Habits",
    "author": "James Clear",
    "price": 15.99,
    "isbn": "9780735211292",
    "publishedDate": "2018-10-16"
}
```
Pagination & Search
```
GET /api/v1/book/?page=1&size=10
GET /api/v1/book/?page=1&size=10&search=atomic
```
---
Authentication Flow
User registers → password hashed with Argon2
User logs in → receives access token (30 min) + refresh token (7 days)
Access token used in `Authorization: Bearer <token>` header
When access token expires → use refresh token to get new one
Logout → refresh token revoked in DB
---
Database Models
User
Field	Type	Description
id	UUID	Primary key
username	String(50)	Unique
email	String(255)	Unique
fullname	String(255)	Optional
password	String(255)	Hashed
role	String(50)	user / admin
is_active	Boolean	Default True
created_at	DateTime	Auto
updated_at	DateTime	Auto
Book
Field	Type	Description
id	UUID	Primary key
user_id	UUID	Foreign key → users
title	String(255)	Required
author	String(255)	Required
price	Float	Required
isbn	String	Unique
published_date	DateTime	Required
created_at	DateTime	Auto
updated_at	DateTime	Auto
---
Author
Built as part of a Backend Development Internship Task.
