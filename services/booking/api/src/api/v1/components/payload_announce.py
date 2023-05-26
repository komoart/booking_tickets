import enum
from datetime import datetime

from pydantic import BaseModel


class EventStatus(str, enum.Enum):
    Created = 'Created'
    Alive = 'Alive'
    Closed = 'Closed'
    Done = 'Done'

    def __repr__(self) -> str:
        return f'{self.value}'


class CreatePayload(BaseModel):
    status: EventStatus
    title: str
    description: str
    sub_only: bool
    is_free: bool
    tickets_count: int
    event_time: datetime
    event_location: str


class UpdatePayload(BaseModel):
    status: EventStatus | None
    title: str | None
    description: str | None
    sub_only: bool | None
    is_free: bool | None
    tickets_count: int | None
    event_time: datetime | None
    event_location: str | None


class MultyPayload(BaseModel):
    author: str | None
    movie: str | None
    free: bool | None
    sub: bool | None
    ticket: int | None
    date: datetime | None
    location: str | None
