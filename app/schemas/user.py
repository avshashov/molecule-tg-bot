from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    user_id: int
    full_name: str


class UserCreate(UserBase):
    pass


class User(BaseModel):
    created_at: datetime
    is_active: bool


class UserUpdate(UserBase):
    is_active: bool
