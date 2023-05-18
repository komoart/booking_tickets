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
