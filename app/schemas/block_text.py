from pydantic import BaseModel


class BlockTextBase(BaseModel):
    text: str
    block: str


class BlockTextCreate(BlockTextBase):
    pass


class BlockText(BlockTextBase):
    id: int


class BlockTextUpdate(BaseModel):
    text: str | None = None
    block: str | None = None
