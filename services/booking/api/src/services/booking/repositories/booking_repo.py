from functools import lru_cache
from typing import Any
from uuid import UUID, uuid4

import sqlalchemy.exc as sqlalch_exc
from fastapi import Depends
from sqlalchemy import insert, select, update

import utils.exceptions as exc
from core.logger import get_logger
from db.models.booking import Booking
from db.pg_db import AsyncSession, get_session
from db.redis import CacheProtocol, get_cache
from services.booking import layer_models, layer_payload
from services.booking.repositories import _protocols, rating_repo, user_repo

logger = get_logger(__name__)


class BookingSqlachemyRepository(_protocols.BookingRepositoryProtocol):
    def __init__(self, db_session: AsyncSession, cache: CacheProtocol) -> None:
        self.user_repo = user_repo.get_user_repo()
        self.rating_repo = rating_repo.get_rating_repo()
        self.db = db_session
        self.redis = cache
        logger.info('BookingSqlachemyRepository init ...')

    async def _get_from_cache(self, key: str) -> Any:
        return await self.redis.get(key)

    async def _set_to_cache(self, key: str, data: Any) -> None:
        await self.redis.set(key, data)

    async def _get_booking_resp(self, data: dict) -> layer_models.BookingResponse:
        """
        Служебный метод. Подготавливает данные и возвращает BookingResponse.

        :param data: layer_models.PGBooking.dict()
        :return: BookingResponse
        """
        _booking = layer_models.PGBooking(**data)

        _author = await self.user_repo.get_by_id(_booking.author_id)
        logger.info(f'Get user <{_booking.author_id}>: <{_author}>')

        _guest = await self.user_repo.get_by_id(_booking.guest_id)
        logger.info(f'Get user <{_booking.guest_id}>: <{_guest}>')

        return layer_models.BookingResponse(
            id=_booking.id,
            author_name=_author.user_name,
            guest_name=_guest.user_name,
            author_status=_booking.author_status,
            guest_status=_booking.guest_status,
        )

    async def get_confirmed_list(self, announce_id: str | UUID) -> list[layer_models.PGBooking]:
        """Получение подтвержденных заявок.

        :param announce_id: id объявления
        :return список подтвержденных заявок
        """
        _query = (
            select(Booking)
            .where(Booking.announcement_id == announce_id)
            .filter(Booking.author_status, Booking.guest_status)
        )
        _res = await self.db.execute(_query)
        scalar_result = [data._asdict() for data in _res.scalars().all()]

        if len(scalar_result) == 0:
            return []
        return [layer_models.PGBooking(**data) for data in scalar_result]

    async def get_by_id(self, booking_id: str | UUID) -> layer_models.PGBooking:
        """Получение полной информации о Booking.

        :param booking_id: id заявки
        :return: layer_models.PGBooking
        :raises NotFoundError: если указаная запись не была найдена в базе
        """
        data = await self.db.get(Booking, booking_id)
        if data is None:
            logger.info(f'[-] Not found <{booking_id}>')
            raise exc.NotFoundError
        return layer_models.PGBooking(**data._asdict())

    async def create(self, announce: layer_payload.AnnounceToCreate, user_id: str | UUID) -> str | UUID:
        """Создание новой записи в БД.

        :param announce: layer_payload.AnnounceToCreate
        :param user_id: id гостя
        :return booking_id: id заявки
        :raises UniqueConstraintError: если запист уже существует в базе
        """
        booking_id = str(uuid4())
        values = layer_payload.PGCreatePayload(
            id=booking_id,
            announcement_id=announce.announce_id,
            movie_id=announce.movie_id,
            author_id=announce.author_id,
            guest_id=user_id,
            event_time=announce.event_time,
        )
        query = insert(Booking).values(**values.dict())
        try:
            await self.db.execute(query)
            await self.db.commit()
            logger.info(f'Create booking <{booking_id}>')

            return booking_id
        except sqlalch_exc.IntegrityError as ex:
            logger.info(f'UniqueConstraintError booking <{booking_id}>')
            raise exc.UniqueConstraintError from ex

    async def sudo_get_multy(
        self,
        query: layer_payload.SudoAPIMultyPayload,
    ) -> list[layer_models.BookingResponse]:
        """Служебный метод. Получение заявок по условию.

        :param query: данные для фильтрации запроса к БД
        :return: список заявок
        """
        _query = select(Booking)
        if query.author:
            _query = _query.filter(Booking.author_id == query.author)
        if query.movie:
            _query = _query.filter(Booking.movie_id == query.movie)
        if query.date:
            _query = _query.filter(Booking.event_time == query.date)

        _res = await self.db.execute(_query)
        scalar_result = [data._asdict() for data in _res.scalars().all()]

        if len(scalar_result) == 0:
            logger.info(f'[-] Not found <{query}>')
            return []
        return [await self._get_booking_resp(data) for data in scalar_result]

    async def get_multy(
        self,
        query: layer_payload.APIMultyPayload,
        user_id: str | UUID,
    ) -> list[layer_models.BookingResponse]:
        """Получение заявок по условию.

        :param user_id: id пользователя
        :param query: данные для фильтрации запроса к БД
        :return: список заявок
        """
        _query = select(Booking)
        if query.role.value == 'guest':
            _query = _query.where(Booking.guest_id == user_id)
        elif query.role.value == 'author':
            _query = _query.where(Booking.author_id == user_id)
        else:
            raise exc.ValueMissingError

        if query.movie:
            _query = _query.filter(Booking.movie_id == query.movie)

        if query.date:
            _query = _query.filter(Booking.event_time == query.date)

        _res = await self.db.execute(_query)
        scalar_result = [data._asdict() for data in _res.scalars().all()]

        if len(scalar_result) == 0:
            logger.info(f'[-] Not found <{query}>')
            return []
        return [await self._get_booking_resp(data) for data in scalar_result]

    async def delete(self, booking_id: str | UUID) -> None:
        """
        Удаление записи из БД.

        :param announce_id: id заявки
        :raises NotFoundError: если указаная запись не была найдена в базе
        """
        _data: Booking = await self.db.get(Booking, booking_id)
        await self.db.delete(_data)
        await self.db.commit()
        logger.info(f'Delete booking <{booking_id}>')

    async def update(
        self,
        user_id: str | UUID,
        booking_id: str | UUID,
        new_status: layer_payload.APIUpdatePayload,
    ) -> None:
        """
        Изменить статус в заявке.

        :param booking_id: id заявки
        :param new_status: новый статус
        :raises NotFoundError: если указаная запись не была найдена в базе
        :raises UniqueConstraintError: если запист уже существует в базе
        """
        query = update(Booking).where(Booking.id == booking_id)
        booking: layer_models.PGBooking = await self.get_by_id(booking_id)
        if user_id == str(booking.author_id):
            if new_status.my_status == booking.author_status:
                return
            query = query.values(
                {'author_status': new_status.my_status},
            )
        elif user_id == str(booking.guest_id):
            if new_status.my_status == booking.guest_status:
                return
            query = query.values(
                {'guest_status': new_status.my_status},
            )
        try:
            await self.db.execute(query)
            await self.db.commit()
            logger.info(f'Update booking <{booking_id}>')
        except sqlalch_exc.IntegrityError as ex:
            logger.info(f'UniqueConstraintError booking <{booking_id}>')
            raise exc.UniqueConstraintError from ex


@lru_cache()
def get_booking_repo(
    db_session: AsyncSession = Depends(get_session),
) -> _protocols.BookingRepositoryProtocol:
    cache: CacheProtocol = get_cache()
    return BookingSqlachemyRepository(db_session, cache)
