from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings
from db.models import announcement, booking

engine = create_async_engine(settings.postgres.a_uri, echo=True)
Base = declarative_base()
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
