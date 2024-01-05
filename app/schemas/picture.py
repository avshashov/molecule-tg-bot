from datetime import datetime

from pydantic import BaseModel


class PictureBase(BaseModel):
    title: str
    description: str
    picture_id: str


class PictureCreate(PictureBase):
    pass


class Picture(PictureBase):
    created_at: datetime


class PictureUpdate(BaseModel):
    description: str | None = None
    title: str | None = None
