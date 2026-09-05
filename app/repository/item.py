from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Item
from app.schemas import ItemCreate, ItemUpdate


async def get_by_id(db: AsyncSession, item_id: int) -> Item | None:
    return await db.get(Item, item_id)


async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Item]:
    result = await db.execute(select(Item).offset(skip).limit(limit))
    return list(result.scalars().all())


async def create(db: AsyncSession, data: ItemCreate, owner_id: int) -> Item:
    item = Item(**data.model_dump(), owner_id=owner_id)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


async def update(db: AsyncSession, item: Item, data: ItemUpdate) -> Item:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    await db.commit()
    await db.refresh(item)
    return item


async def delete(db: AsyncSession, item: Item) -> None:
    await db.delete(item)
    await db.commit()
