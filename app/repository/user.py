from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models import User
from app.schemas import UserCreate


async def get_by_username(db: AsyncSession, username: str) -> User | None:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def create(db: AsyncSession, data: UserCreate) -> User:
    user = User(username=data.username, hashed_password=await hash_password(data.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
