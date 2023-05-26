from functools import lru_cache
from typing import Any
from uuid import UUID, uuid4

import sqlalchemy.exc as sqlalch_exc
from fastapi import Depends
from sqlalchemy import insert, select, update

import utils.exceptions as exc
from core.config import settings
from core.logger import get_logger
from db.models.announcement import Announcement
from db.pg_db import AsyncSession, get_session
from db.redis import CacheProtocol, get_cache
from services.announcement import layer_models, layer_payload
from services.announcement.repositories import _protocols

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

    async def get_by_id(self, announce_id: str | UUID) -> layer_models.PGAnnouncement:
        """
        Получение записи Announcement из БД.

        :param announce_id: id объявления
        :return: layer_models.PGAnnouncement
        :raises NotFoundError: если указаная запись не была найдена в базе
        """
        try:
            data = await self.db.get(Announcement, announce_id)
            if data is None:
                logger.info(f'[-] Not found <{announce_id}>')
                raise exc.NotFoundError
            return data
        except exc.NotFoundError:
            raise

    async def create(
        self,
        new_announce: layer_payload.PGCreatePayload,
        movie: layer_models.MovieToResponse,
        author_id: str | UUID,
    ) -> str | UUID:
        """
        Создание новой записи в БД.

        :param author_id: id автора
        :param movie: информация о фильме
        :param new_announce: данные для создания объявления
        :return announce_id: id объявления
        :raises UniqueConstraintError: если запист уже существует в базе
        """
        _id = str(uuid4())
        values = layer_payload.PGCreatePayload(
            id=_id,
            movie_id=movie.movie_id,
            author_id=author_id,
            duration=movie.duration,
            **new_announce.dict(),
        ).dict()
        query = insert(Announcement).values(**values)
        try:
            await self.db.execute(query)
            await self.db.commit()
            logger.info(f'Create announcement <{_id}>')

            return _id
        except sqlalch_exc.IntegrityError as ex:
            logger.info(f'UniqueConstraintError announcement <{_id}>')
            raise exc.UniqueConstraintError from ex

    async def get_multy(
        self,
        query: layer_payload.APIMultyPayload,
        user: layer_models.UserToResponse,
    ) -> list[layer_models.AnnouncementResponse | None]:
        """
        Получение объявлений по условию.

        :param user: информация о пользователе
        :param query: данные для фильтрации запроса к БД
        :return: список объявлений
        """
        _query = select(Announcement)

        if not settings.debug.DEBUG:
            _query = _query.filter(Announcement.status == layer_models.EventStatus.Alive.value)

        if query.sub:
            _sub = user.subs
            _query = _query.where(Announcement.author_id.in_(_sub))
        if query.author:
            _query = _query.filter(Announcement.author_id == query.author)
        if query.movie:
            _query = _query.filter(Announcement.movie_id == query.movie)
        if query.free:
            _query = _query.filter(Announcement.is_free is query.free)
        if query.ticket:
            _query = _query.filter(Announcement.tickets_count == query.ticket)
        if query.date:
            _query = _query.filter(Announcement.event_time == query.date)
        if query.location:
            _query = _query.filter(Announcement.event_location == query.location)

        _res = await self.db.execute(_query)
        scalar_result = [data._asdict() for data in _res.scalars().all()]

        if len(scalar_result) == 0:
            logger.info(f'[-] Not found <{query}>')
            return []
        return [layer_models.AnnouncementResponse(**data) for data in scalar_result]

    async def update(
        self,
        announce_id: str | UUID,
        update_announce: layer_payload.APIUpdatePayload,
    ) -> None:
        """
        Изменить данные в объявлении.

        :param announce_id: id объявления
        :param update_announce: данные для изменения объявления
        :raises NotFoundError: если указаная запись не была найдена в базе
        :raises UniqueConstraintError: если запист уже существует в базе
        """
        query = (
            update(Announcement).where(Announcement.id == announce_id).values(update_announce.dict(exclude_none=True))
        )
        try:
            await self.db.execute(query)
            await self.db.commit()
            logger.info(f'Update announcement <{announce_id}>')
        except sqlalch_exc.IntegrityError as ex:
            logger.info(f'UniqueConstraintError announcement <{announce_id}>')
            raise exc.UniqueConstraintError from ex

    async def delete(self, announce_id: str | UUID) -> None:
        """
        Удаление записи из БД.

        :param announce_id: id объявления
        :raises NotFoundError: если указаная запись не была найдена в базе
        """
        _data: Announcement = await self.db.get(Announcement, announce_id)
        await self.db.delete(_data)
        await self.db.commit()
        logger.info(f'Delete announcement <{announce_id}>')


@lru_cache()
def get_announcement_repo(
    db_session: AsyncSession = Depends(get_session),
) -> _protocols.AnnouncementRepositoryProtocol:
    cache: CacheProtocol = get_cache()
    return AnnounceSqlachemyRepository(db_session, cache)
