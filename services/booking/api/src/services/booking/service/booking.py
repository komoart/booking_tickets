from enum import Enum
from typing import Any
from uuid import UUID
from functools import lru_cache

from fastapi import Depends

from core.logger import get_logger
from db.redis import CacheProtocol, get_cache

logger = get_logger(__name__)


class Permission(int, Enum):
    super = 0
    author = 1
    guest = 2


class BookingService:
    def __init__(
        self,
        cache: CacheProtocol,
    ) -> None:
        self.redis = cache
        logger.info('BookingServic init ...')

    async def _get_from_cache(self, key: str) -> Any:
        return await self.redis.get(key)

    async def _set_to_cache(self, key: str, data: Any) -> None:
        await self.redis.set(key, data)

    async def _check_permissions(self, user: dict, booking_id: str | UUID) -> Permission:
        pass

    async def create(
        self,
        announce_id: str | UUID,
        user: dict,
    ):
        pass


@lru_cache()
def get_booking_service(
    cache: CacheProtocol = Depends(get_cache),
) -> BookingService:
    return BookingService(cache)
