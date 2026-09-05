from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ItemBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=128)
    description: str | None = Field(default=None, max_length=512)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=128)
    description: str | None = Field(default=None, max_length=512)


class ItemOut(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    created_at: datetime
