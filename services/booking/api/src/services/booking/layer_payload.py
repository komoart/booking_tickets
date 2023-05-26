from datetime import datetime
from enum import Enum
from typing import Union
from uuid import UUID

from pydantic import BaseModel


class Role(str, Enum):
    guest = 'guest'
    author = 'author'

    def __repr__(self) -> str:
        return f'{self.value}'


class APIUpdatePayload(BaseModel):
    my_status: bool


class SudoAPIMultyPayload(BaseModel):
    is_self: bool | None
    author: str | None
    movie: str | None
    date: datetime | None


class APIMultyPayload(BaseModel):
    role: Role
    movie: str | None
    date: datetime | None


class EventStatus(str, Enum):
    Created = 'Created'
    Alive = 'Alive'
    Closed = 'Closed'
    Done = 'Done'

    def __repr__(self) -> str:
        return f'{self.value}'


class AnnounceToCreate(BaseModel):
    status: EventStatus
    announce_id: str | UUID
    author_id: str | UUID
    movie_id: str | UUID
    event_time: datetime


class PGCreatePayload(BaseModel):
    id: str | UUID
    announcement_id: str | UUID
    movie_id: str | UUID
    author_id: str | UUID
    guest_id: str | UUID
    event_time: datetime


class DeleteBooking(BaseModel):
    del_booking_announce_id: str | UUID
    guest_name: str
    user_id: str | UUID


class NewBooking(BaseModel):
    new_booking_id: str | UUID
    announce_id: str | UUID
    user_id: str | UUID


class StatusBooking(BaseModel):
    status_booking_id: str | UUID
    announce_id: str | UUID
    user_id: str | UUID
    another_id: str | UUID


context = Union[DeleteBooking, NewBooking, StatusBooking]


class EventType(str, Enum):
    booking_new = 'booking_new'
    booking_status = 'booking_status'
    booking_delete = 'booking_delete'

    def __repr__(self) -> str:
        return f'{self.value}'


class NotificEvent(BaseModel):
    notification_id: str
    source_name: str
    event_type: EventType
    context: context
    created_at: datetime

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['created_at'] = _dict['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        return _dict
