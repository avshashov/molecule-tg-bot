from enum import Enum


class PictureStatus(str, Enum):
    READY = 'ready'
    ORDER = 'order'
    RENT = 'rent_order'


class MediaBlock(int, Enum):
    RENT = 1
    PICTURE = 2
    ABOUT_PROJECT = 3


class MediaType(int, Enum):
    PHOTO = 1
    PRESENTATION = 2


class BlockText(str, Enum):
    RENT = 'Аренда'
    CONTACTS = 'Контакты'
