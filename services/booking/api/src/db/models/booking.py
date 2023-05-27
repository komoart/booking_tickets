import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, UniqueConstraint, inspect, MetaData
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

from db.models.announcement import Announcement

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Booking(Base):
    __tablename__ = 'booking'
    __table_args__ = (
        UniqueConstraint('guest_id', 'event_time', name='_bk_guest_event_time'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    announcement_id = Column(UUID(as_uuid=True), ForeignKey(Announcement.id, ondelete='cascade'), nullable=False)
    movie_id = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True)
    author_id = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True)
    guest_id = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True)
    author_status = Column(Boolean, nullable=True, default=None)
    guest_status = Column(Boolean, server_default='t', default=True)
    event_time = Column(TIMESTAMP(timezone=True), nullable=False)
    created = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    modified = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    def _asdict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
