from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class RatingToResponse(BaseModel):
    user_rating: float


class UserToResponse(BaseModel):
    user_id: str | UUID
    user_name: str
    subs: list[str | UUID]


class BookingToDetailResponse(BaseModel):
    booking_id: str | UUID
    guest_id: str | UUID
    guest_name: str
    guest_rating: float
    guest_status: bool
    author_status: bool | None


class MovieToResponse(BaseModel):
    movie_id: str | UUID
    movie_title: str
    duration: int


class EventStatus(str, Enum):
    Created = 'Created'
    Alive = 'Alive'
    Closed = 'Closed'
    Done = 'Done'

    def __repr__(self) -> str:
        return f'{self.value}'


class AnnouncementResponse(BaseModel):
    id: str | UUID
    title: str
    author_id: str | UUID
    sub_only: bool
    is_free: bool
    tickets_count: int
    event_time: datetime
    event_location: str
    duration: int


class DetailAnnouncementResponse(BaseModel):
    id: str | UUID
    created: datetime
    modified: datetime
    status: EventStatus
    title: str
    description: str
    movie_title: str
    author_name: str
    sub_only: bool
    is_free: bool
    tickets_count: int
    tickets_left: int
    event_time: datetime
    event_location: str
    guest_list: list[BookingToDetailResponse]
    author_rating: float
    duration: int


class PGAnnouncement(BaseModel):
    id: str | UUID
    created: datetime
    modified: datetime
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


class AnnouncementToReviewResponse(BaseModel):
    author_id: str | UUID
    guest_id: str | UUID
    announcement_id: str | UUID
    author_name: str
    guest_name: str
    announcement_title: str
