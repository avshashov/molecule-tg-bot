from datetime import datetime

from sqlalchemy import BigInteger, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


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

    media_id: Mapped[str] = mapped_column(unique=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    media_type_id: Mapped[int] = mapped_column(
        ForeignKey('media_type.id', ondelete='CASCADE')
    )
    media_block_id: Mapped[int] = mapped_column(
        ForeignKey('media_block.id', ondelete='CASCADE')
    )

    media_type: Mapped['MediaType'] = relationship('MediaType', backref='media')
    media_block: Mapped['MediaBlock'] = relationship('MediaBlock', backref='media')


class MediaType(Base):
    __tablename__ = 'media_type'

    type: Mapped[str]


class MediaBlock(Base):
    __tablename__ = 'media_block'

    block: Mapped[str]


class Picture(Base):
    __tablename__ = 'picture'

    picture_id: Mapped[str] = mapped_column(unique=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())


class BlockText(Base):
    __tablename__ = 'block_text'

    block: Mapped[str] = mapped_column(nullable=False, unique=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
