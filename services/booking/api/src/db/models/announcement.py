import enum
import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, Boolean, Column, Enum, Integer, String, UniqueConstraint, inspect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class EventStatus(enum.Enum):
    Created = 'Created'
    Alive = 'Alive'
    Closed = 'Closed'
    Done = 'Done'


class Announcement(Base):
    __tablename__ = 'announcements'
    __table_args__ = (UniqueConstraint('author_id', 'event_time', name='_author_event_time'),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    status = Column(Enum(EventStatus))
    title = Column(String(256), default='test_title')
    description = Column(String(4096), default='test_description')
    movie_id = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True)
    author_id = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True)
    sub_only = Column(Boolean, server_default='t', default=True)
    is_free = Column(Boolean, server_default='t', default=True)
    tickets_count = Column(Integer, default=1)
    event_time = Column(TIMESTAMP(timezone=True), nullable=False, unique=True)
    event_location = Column(String(4096), default='test_location')
    created = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    modified = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    duration = Column(Integer, default=60)

    def _asdict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
