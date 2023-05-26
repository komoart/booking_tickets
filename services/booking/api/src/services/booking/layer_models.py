from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class MovieToResponse(BaseModel):
    movie_id: str | UUID
    movie_title: str
    duration: int


class RatingToResponse(BaseModel):
    user_rating: float


class UserToResponse(BaseModel):
    user_id: str | UUID
    user_name: str
    subs: list[str | UUID]


class EventStatus(str, Enum):
    Created = 'Created'
    Alive = 'Alive'
    Closed = 'Closed'
    Done = 'Done'

    def __repr__(self) -> str:
        return f'{self.value}'


class AnnounceToResponse(BaseModel):
    status: EventStatus
    announce_id: str | UUID
    author_id: str | UUID
    movie_id: str | UUID
    event_time: datetime
    tickets_count: int


class BookingResponse(BaseModel):
    id: str | UUID
    author_name: str
    guest_name: str
    author_status: bool | None
    guest_status: bool


class DetailBookingResponse(BaseModel):
    id: str | UUID
    announcement_id: str | UUID
    movie_title: str
    author_name: str
    guest_name: str
    author_status: bool | None = None
    guest_status: bool = True
    guest_rating: float
    author_rating: float
    event_time: datetime


class PGBooking(BaseModel):
    id: str | UUID
    created: datetime
    modified: datetime
    announcement_id: str | UUID
    movie_id: str | UUID
    author_id: str | UUID
    guest_id: str | UUID
    author_status: bool | None
    guest_status: bool | None
    event_time: datetime
