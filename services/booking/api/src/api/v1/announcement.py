from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query

import utils.exceptions as exc
from api.v1.components import payload_announce, resp_announce
from core.config import settings
from services.announcement.service.announcement import (AnnouncementService,
                                                        get_announcement_service)
from utils import auth

router = APIRouter()
auth_handler = auth.AuthHandler()


@router.post(
    '/announcement/{movie_id}',
    summary='Создать объявление',
    description='Создание записи в DB',
    response_model=resp_announce.DetailAnnouncementResponse,
    response_description='Подробная информация из объявления',
)
async def create(
    movie_id: str,
    payload: payload_announce.CreatePayload,
    announcement_service: AnnouncementService = Depends(get_announcement_service),
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> resp_announce.DetailAnnouncementResponse:
    if settings.debug.DEBUG:
        payload = payload_announce.CreatePayload(
            status=payload_announce.EventStatus.Created,
            title='Fake Title',
            description='Fake description',
            sub_only=False,
            is_free=True,
            tickets_count=2,
            event_time=datetime.now(),
            event_location='Fake location',
        )
    try:
        return await announcement_service.create(
            author_id=_user.get('user_id'),
            movie_id=movie_id,
            new_announce=payload,
        )
    except exc.UniqueConstraintError:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
