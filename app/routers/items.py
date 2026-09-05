from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models import User
from app.repository import item as item_repo
from app.schemas import ItemCreate, ItemOut, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[ItemOut])
async def list_items(
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[User, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100,
):
    return await item_repo.get_all(db, skip=skip, limit=limit)


@router.get("/{item_id}", response_model=ItemOut)
async def get_item(item_id: int, db: Annotated[AsyncSession, Depends(get_db)], _: Annotated[User, Depends(get_current_user)]):
    item = await item_repo.get_by_id(db, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.post("", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
async def create_item(
    data: ItemCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await item_repo.create(db, data, owner_id=current_user.id)


@router.put("/{item_id}", response_model=ItemOut)
async def update_item(
    item_id: int,
    data: ItemUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[User, Depends(get_current_user)],
):
    item = await item_repo.get_by_id(db, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return await item_repo.update(db, item, data)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: Annotated[AsyncSession, Depends(get_db)], _: Annotated[User, Depends(get_current_user)]):
    item = await item_repo.get_by_id(db, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    await item_repo.delete(db, item)
