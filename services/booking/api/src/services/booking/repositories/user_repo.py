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


class UserMockRepository(_protocols.UserRepositoryProtocol):
    def __init__(self, cache: CacheProtocol) -> None:
        self.auth_endpoint = f'{settings.auth.uri}user_info/'
        self.ugc_endpoint = f'{settings.ugc.uri}subscribers/'
        self._headers = _headers()
        self.redis = cache

        logger.info('UserMockRepository init ...')

    async def _get_from_cache(self, key: str) -> Any:
        return await self.redis.get(key)

    async def _set_to_cache(self, key: str, data: Any) -> None:
        await self.redis.set(key, data)

    async def get_by_id(self, user_id: str | UUID) -> layer_models.UserToResponse:
        if _cache := await self._get_from_cache(f'user:{user_id}'):
            logger.info('MovieToResponse from cache')
            return layer_models.UserToResponse(**_cache)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'{self.auth_endpoint}{user_id}',
                    headers=self._headers,
                ) as resp:
                    _user = await resp.json()
                    logger.debug(f'Get user <{user_id}>: <{_user}>')
                async with session.post(
                    f'{self.ugc_endpoint}{user_id}',
                    headers=self._headers,
                ) as resp:
                    _subs = await resp.json()
                    logger.debug(f'Get subs for user <{user_id}>: <{_subs}>')

        except ClientError as ex:  # noqa: F841
            logger.debug(f'Except <{ex}>')
            return None
        data = layer_models.UserToResponse(
            user_id=str(user_id),
            user_name=f"{_user.get('name')} {_user.get('last_name')}",
            subs=_subs,
        )
        await self._set_to_cache(f'user:{user_id}', data.dict())
        logger.info('UserToResponse set to cache')
        return data


@lru_cache()
def get_user_repo() -> _protocols.UserRepositoryProtocol:
    cache: CacheProtocol = get_cache()
    return UserMockRepository(cache)
