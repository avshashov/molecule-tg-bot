from pydantic import BaseModel


class BlockTextBase(BaseModel):
    text: str
    block: str


class BlockTextCreate(BlockTextBase):
    pass
