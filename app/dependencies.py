import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password
from app.db.session import get_db
from app.models import User
from app.repository import user as user_repo

security = HTTPBasic()


async def get_current_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    user = await user_repo.get_by_username(db, credentials.username)
    if user is None or not await verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    if not secrets.compare_digest(user.username, credentials.username):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user
