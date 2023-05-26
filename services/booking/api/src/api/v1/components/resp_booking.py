from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


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
    author_status: bool | None
    guest_status: bool
    guest_rating: float
    author_rating: float
    event_time: datetime
