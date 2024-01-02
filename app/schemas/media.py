from datetime import datetime

from pydantic import BaseModel


class MediaBase(BaseModel):
    title: str
    description: str | None = None
    media_id: int


class MediaCreate(MediaBase):
    media_type_id: int
    media_block_id: int


class Media(MediaBase):
    created_at: datetime


class MediaUpdate(BaseModel):
    media_id: str | None = None
    description: str | None = None
    title: str | None = None
