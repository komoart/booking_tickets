from functools import lru_cache
from typing import Any
from uuid import UUID

import aiohttp
from aiohttp.client_exceptions import ClientError

from core.config import settings
from core.logger import get_logger
from db.redis import CacheProtocol, get_cache
from services.booking import layer_models
from services.booking.repositories import _protocols
from utils.auth import _headers

logger = get_logger(__name__)


class MovieMockRepository(_protocols.MovieRepositoryProtocol):
    def __init__(self, cache: CacheProtocol) -> None:
        self.movie_endpoint = f'{settings.movie_api.uri}movie/'
        self._headers = _headers()
        self.redis = cache

        logger.info('MovieMockRepository init ...')

    async def _get_from_cache(self, key: str) -> Any:
        return await self.redis.get(key)

    async def _set_to_cache(self, key: str, data: Any) -> None:
        await self.redis.set(key, data)

    async def get_by_id(self, movie_id: str | UUID) -> layer_models.MovieToResponse:
        if _cache := await self._get_from_cache(f'movie:{movie_id}'):
            logger.info('MovieToResponse from cache')
            return layer_models.MovieToResponse(**_cache)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'{self.movie_endpoint}{movie_id}',
                    headers=self._headers,
                ) as resp:
                    _movie = await resp.json()
                    logger.debug(f'Get movie <{movie_id}>: <{_movie}>')
                    _duration = _movie.get('duration')
                    if settings.debug.DEBUG:
                        _duration = 0

        except ClientError as ex:  # noqa: F841
            logger.debug(f'Except <{ex}>')
            return None
        data = layer_models.MovieToResponse(
            movie_id=str(movie_id),
            movie_title=_movie.get('title'),
            duration=_duration,
        )
        await self._set_to_cache(f'movie:{movie_id}', data.dict())
        logger.info('MovieToResponse set to cache')
        return data


@lru_cache()
def get_movie_repo() -> _protocols.MovieRepositoryProtocol:
    cache: CacheProtocol = get_cache()
    return MovieMockRepository(cache)
