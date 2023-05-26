import enum
from datetime import datetime
from typing import Union
from uuid import UUID

from pydantic import BaseModel


class EventStatus(str, enum.Enum):
    Created = 'Created'
    Alive = 'Alive'
    Closed = 'Closed'
    Done = 'Done'


class APICreatePayload(BaseModel):
    status: EventStatus
    title: str
    description: str
    sub_only: bool
    is_free: bool
    tickets_count: int
    event_time: datetime
    event_location: str


class PGCreatePayload(BaseModel):
    id: str | UUID
    status: EventStatus
    title: str
    description: str
    movie_id: str | UUID
    author_id: str | UUID
    sub_only: bool
    is_free: bool
    tickets_count: int
    event_time: datetime
    event_location: str
    duration: int


class APIUpdatePayload(BaseModel):
    status: EventStatus | None
    title: str | None
    description: str | None
    sub_only: bool | None
    is_free: bool | None
    tickets_count: int | None
    event_time: datetime | None
    event_location: str | None


class APIMultyPayload(BaseModel):
    author: str | None
    movie: str | None
    free: bool | None
    sub: bool | None
    ticket: int | None
    date: datetime | None
    location: str | None


class NewAnnounce(BaseModel):
    new_announce_id: str | UUID
    user_id: str | UUID


class PutAnnounce(BaseModel):
    put_announce_id: str | UUID
    user_id: str | UUID


class DeleteAnnounce(BaseModel):
    delete_announce_id: str | UUID
    author_name: str
    announce_title: str
    user_id: str | UUID


class DoneAnnounce(BaseModel):
    done_announce_id: str | UUID
    user_id: str | UUID


context = Union[
    NewAnnounce,
    PutAnnounce,
    DeleteAnnounce,
    DoneAnnounce,
]


class EventType(str, enum.Enum):
    announce_new = 'announce_new'
    announce_put = 'announce_put'
    announce_done = 'announce_done'
    announce_delete = 'announce_delete'

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
