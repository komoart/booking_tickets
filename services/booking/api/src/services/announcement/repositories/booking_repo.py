from functools import lru_cache
from typing import Any
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select

from core.logger import get_logger
from db.models.booking import Booking
from db.pg_db import AsyncSession, get_session
from db.redis import CacheProtocol, get_cache
from services.announcement import layer_models
from services.announcement.repositories import _protocols, rating_repo, user_repo

logger = get_logger(__name__)


class BookingMockRepository(_protocols.BookingRepositoryProtocol):
    def __init__(self, cache: CacheProtocol) -> None:
        self.user_repo = user_repo.get_user_repo()
        self.rating_repo = rating_repo.get_rating_repo()
        self.redis = cache
        logger.info('BookingMockRepository init ...')

    async def _get_from_cache(self, key: str) -> Any:
        return await self.redis.get(key)

    async def _set_to_cache(self, key: str, data: Any) -> None:
        await self.redis.set(key, data)

    async def _fake_boking(self) -> layer_models.BookingToDetailResponse:
        return layer_models.BookingToDetailResponse(
            guest_name=await self.user_repo.get_by_id('fake_uuid'),
            guest_rating=await self.rating_repo.get_by_id('fake_uuid'),
            guest_status=True,
            author_status=True,
        )

    async def get_by_id(self, announce_id: str | UUID) -> list[layer_models.BookingToDetailResponse]:
        return [await self._fake_boking() for _ in range(5)]


class BookingSqlachemyRepository(_protocols.BookingRepositoryProtocol):
    def __init__(self, db_session: AsyncSession, cache: CacheProtocol) -> None:
        self.user_repo = user_repo.get_user_repo()
        self.rating_repo = rating_repo.get_rating_repo()
        self.db = db_session
        self.redis = cache
        logger.info('BookingSqlachemyRepository init ...')
        ...

    async def _get_from_cache(self, key: str) -> Any:
        return await self.redis.get(key)

    async def _set_to_cache(self, key: str, data: Any) -> None:
        await self.redis.set(key, data)

    async def _get_booking_resp(self, data: dict) -> layer_models.BookingToDetailResponse:
        """
        Служебный метод. Возвращает данные для layer_models.DetailBookingResponse.

        :param data: layer_models.PGBookin.dict()
        :param user: информация о пользователе
        :return: данные для layer_models.DetailBookingResponse
        """

        _booking = layer_models.PGBooking(**data)

        _guest = await self.user_repo.get_by_id(_booking.guest_id)
        logger.info(f'Get user <{_booking.guest_id}>: <{_guest}>')

        _guest_rating = await self.rating_repo.get_by_id(_booking.guest_id)

        return layer_models.BookingToDetailResponse(
            booking_id=_booking.id,
            guest_id=_booking.guest_id,
            guest_name=_guest.user_name,
            guest_rating=_guest_rating.user_rating,
            guest_status=_booking.guest_status,
            author_status=_booking.author_status,
        )

    async def get_by_id(self, announce_id: str | UUID) -> list[layer_models.BookingToDetailResponse]:
        """
        Возвращает данные для layer_models.DetailBookingResponse.

        :param announce_id: lid объявления
        :return: список данных для layer_models.DetailBookingResponse
        """
        _query = select(Booking).filter(Booking.announcement_id == announce_id)
        _res = await self.db.execute(_query)
        scalar_result = [data._asdict() for data in _res.scalars().all()]

        if len(scalar_result) == 0:
            return []
        return [await self._get_booking_resp(data) for data in scalar_result]

    async def get_confirmed_list(self, announce_id: str | UUID) -> list[layer_models.BookingToDetailResponse]:
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
        return [await self._get_booking_resp(data) for data in scalar_result]

    async def get_guest_id(self, booking_id: str | UUID) -> str | UUID:
        data: layer_models.PGBooking = await self.db.get(Booking, booking_id)
        return data.guest_id


@lru_cache()
def get_booking_repo(
    db_session: AsyncSession = Depends(get_session),
) -> _protocols.BookingRepositoryProtocol:
    cache: CacheProtocol = get_cache()
    return BookingSqlachemyRepository(db_session, cache)
