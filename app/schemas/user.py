from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=64)
    password: str = Field(..., min_length=4, max_length=72)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    is_active: bool
    created_at: datetime
