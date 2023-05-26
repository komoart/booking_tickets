from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Role(str, Enum):
    guest = 'guest'
    author = 'author'


class UpdatePayload(BaseModel):
    my_status: bool


class SudoMultyPayload(BaseModel):
    is_self: bool | None
    author: str | None
    movie: str | None
    date: datetime | None


class MultyPayload(BaseModel):
    role: Role
    movie: str | None
    date: datetime | None
