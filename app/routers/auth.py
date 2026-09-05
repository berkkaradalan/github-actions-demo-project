from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models import User
from app.repository import user as user_repo
from app.schemas import UserCreate, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBasic()


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    if await user_repo.get_by_username(db, data.username) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already taken")
    return await user_repo.create(db, data)


@router.post("/login", response_model=UserOut)
async def login(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await get_current_user(credentials, db)


@router.get("/me", response_model=UserOut)
async def me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
