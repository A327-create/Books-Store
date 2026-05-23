from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.core.database import engine, Base
from fastapi_pagination import add_pagination
from app.api.v1.user_routes import router as user_routes
from app.api.v1.auth_routes import router as auth_routes
from app.api.v1.book_routes import router as book_routes
from app.api.v1.admin.user_routes import router as admin_user_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    #startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
app = FastAPI(
    title=settings.APPNAME,
    # version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)
add_pagination(app)
app.include_router(auth_routes, prefix='/api/v1')
app.include_router(user_routes, prefix='/api/v1')
app.include_router(book_routes, prefix='/api/v1')
app.include_router(admin_user_routes, prefix='/api/v1')

@app.get("/health")
async def health_check():
    return {"status": "ok"}