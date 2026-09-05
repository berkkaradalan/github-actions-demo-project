"""
TEST: GITHUB ACTIONS PIPELINE 1.0
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.db.base import Base
from app.db.session import AsyncSessionLocal, engine
from app.models import Item, User  # noqa: F401 (register tables on Base.metadata)
from app.repository import user as user_repo
from app.routers import auth, items
from app.schemas import UserCreate


async def seed_default_user() -> None:
    async with AsyncSessionLocal() as db:
        if await user_repo.get_by_username(db, settings.default_admin_user) is None:
            await user_repo.create(
                db,
                UserCreate(username=settings.default_admin_user, password=settings.default_admin_password),
            )


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await seed_default_user()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.include_router(auth.router)
app.include_router(items.router)


@app.get("/health", tags=["health"])
async def health() -> dict:
    return {"status": "ok"}
