from functools import lru_cache
from typing import Any
from uuid import UUID

from fastapi import Depends
from sqlalchemy import update

import utils.exceptions as exc
from core.logger import get_logger
from db.models.announcement import Announcement
from db.pg_db import AsyncSession, get_session
from db.redis import CacheProtocol, get_cache
from services.booking import layer_models
from services.booking.repositories import _protocols

logger = get_logger(__name__)


class AnnounceSqlachemyRepository(_protocols.AnnouncementRepositoryProtocol):
    def __init__(self, db_session: AsyncSession, cache: CacheProtocol) -> None:
        self.db = db_session
        self.redis = cache
        logger.info('AnnounceSqlachemyRepository init ...')

    async def _get_from_cache(self, key: str) -> Any:
        return await self.redis.get(key)

    async def _set_to_cache(self, key: str, data: Any) -> None:
        await self.redis.set(key, data)

    async def get_by_id(self, announce_id: str | UUID) -> layer_models.AnnounceToResponse:
        """
        Возвращает данные из БД для layer_models.DetailBookingResponse.

        :param announce_id: lid объявления
        :return: данные для layer_models.DetailBookingResponse
        :raises NotFoundError: если указаная запись не была найдена в базе
        """
        _data = await self.db.get(Announcement, announce_id)
        if _data is None:
            logger.info(f'[-] Not found <{announce_id}>')
            raise exc.NotFoundError
        _data = _data._asdict()

        return layer_models.AnnounceToResponse(
            status=_data.get('status').value,
            announce_id=_data.get('id'),
            author_id=_data.get('author_id'),
            event_time=_data.get('event_time'),
            movie_id=_data.get('movie_id'),
            tickets_count=_data.get('tickets_count'),
        )

    async def set_alive_status(self, announce_id: str | UUID) -> None:
        query = (
            update(Announcement)
            .where(Announcement.id == announce_id)
            .values({'status': layer_models.EventStatus.Alive})
        )
        await self.db.execute(query)
        await self.db.commit()
        logger.info(f'Update announcement <{announce_id}>')

    async def set_closed_status(self, announce_id: str | UUID) -> None:
        query = (
            update(Announcement)
            .where(Announcement.id == announce_id)
            .values({'status': layer_models.EventStatus.Closed})
        )
        await self.db.execute(query)
        await self.db.commit()
        logger.info(f'Update announcement <{announce_id}>')


@lru_cache()
def get_announcement_repo(
    db_session: AsyncSession = Depends(get_session),
) -> _protocols.AnnouncementRepositoryProtocol:
    cache: CacheProtocol = get_cache()
    return AnnounceSqlachemyRepository(db_session, cache)
