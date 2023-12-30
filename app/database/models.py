from datetime import datetime

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = 'user'

    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str]
    full_name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    is_active: Mapped[bool] = mapped_column(default=True)


class Media(Base):
    __tablename__ = 'media'

    media_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    media_name: Mapped[str] = mapped_column(String(length=15), nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())


class Picture(Base):
    __tablename__ = 'picture'

    picture_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    description: Mapped[str]
