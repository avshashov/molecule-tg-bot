from datetime import datetime

from pydantic import BaseModel


class MediaBase(BaseModel):
    media_name: str
    description: str | None = None
    media_id: int


class MediaCreate(MediaBase):
    pass


class Media(MediaBase):
    created_at: datetime


class MediaUpdate(BaseModel):
    media_id: str | None = None
    description: str | None = None
    media_name: str | None = None

