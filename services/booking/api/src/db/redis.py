from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Any

import orjson
from redis import asyncio as aioredis

from core.config import settings


class CacheProtocol(ABC):
    @abstractmethod
    async def get(self, key: str) -> str:
        ...

    @abstractmethod
    async def set(self, key: str, value: Any, exp: int) -> None:
        ...


class RedisCache(CacheProtocol):
    def __init__(self) -> None:
        self.session = aioredis.from_url(settings.redis.uri)

    async def get(self, key: str) -> str:
        value = await self.session.get(key)
        if value is None:
            return None
        return orjson.loads(value)

    async def set(self, key: str, value: Any, exp: int = settings.redis.EXPIRE_SEC) -> None:
        await self.session.set(key, orjson.dumps(value), ex=exp)

    async def close(self) -> None:
        await self.session.close()


@lru_cache()
def get_cache() -> CacheProtocol:
    return RedisCache()
