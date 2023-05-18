from typing import Any
from uuid import UUID
from functools import lru_cache

import pytz
from fastapi import Depends

from core.logger import get_logger
from db.redis import CacheProtocol, get_cache

logger = get_logger(__name__)
utc = pytz.UTC


class AnnouncementService:
    def __init__(
        self,
        cache: CacheProtocol,
    ):
        self.redis = cache
        logger.info('AnnouncementService init ...')

    async def _get_from_cache(self, key: str) -> Any:
        return await self.redis.get(key)

    async def _set_to_cache(self, key: str, data: Any) -> None:
        await self.redis.set(key, data)

    async def _check_permissions(
        self,
        announce_id: str | UUID,
        user: dict,
    ) -> bool:
        pass

    async def create(
        self,
    ):
        pass


@lru_cache()
def get_announcement_service(
    cache: CacheProtocol = Depends(get_cache),
) -> AnnouncementService:
    return AnnouncementService(cache)
