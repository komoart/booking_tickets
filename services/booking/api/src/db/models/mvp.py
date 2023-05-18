import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class MVP(Base):
    __tablename__ = 'mvp'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    some_int = Column(Integer, default=0)
    some_str = Column(String(4096), default='test')
    created = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    modified = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
