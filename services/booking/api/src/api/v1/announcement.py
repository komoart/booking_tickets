from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query

import utils.exceptions as exc
from api.v1.components import payload_announce, resp_announce
from core.config import settings
from services.announcement.service.announcement import AnnouncementService, get_announcement_service
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


@router.put(
    '/announcement/{announcement_id}',
    summary='Изменить объявление',
    description='Изменение записи в DB',
    response_model=resp_announce.DetailAnnouncementResponse,
    response_description='Подробная информация после изменения',
)
async def update(
    announcement_id: str,
    payload: payload_announce.UpdatePayload,
    announcement_service: AnnouncementService = Depends(get_announcement_service),
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> resp_announce.DetailAnnouncementResponse:
    try:
        await announcement_service.update(
            user=_user,
            announce_id=announcement_id,
            payload=payload,
        )
        return await announcement_service.get_one(announcement_id)
    except exc.NotFoundError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    except exc.UniqueConstraintError:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
    except exc.NoAccessError:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN)


@router.get(
    '/announcement/{announcement_id}',
    summary='Получить объявление по id',
    description='Получение всей информации по объявлению, сервис идет за информацией в db, UGC, Auth, Movie_api',
    response_model=resp_announce.DetailAnnouncementResponse,
    response_description='Подробная информация из объявления',
)
async def get_one(
    announcement_id: str,
    announcement_service: AnnouncementService = Depends(get_announcement_service),
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> resp_announce.DetailAnnouncementResponse:
    try:
        return await announcement_service.get_one(announce_id=announcement_id)
    except exc.NotFoundError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)


@router.get(
    '/announcements',
    summary='Получить список всех объявлений',
    description='Получение списка объявлений, сервис идет за информацией в db',
    response_model=list[resp_announce.AnnouncementResponse],
    response_description='Список объявлений по условию',
)
async def get_multy(
    _author: str | None = Query(default=None, alias='filter[author]'),
    _movie: str | None = Query(default=None, alias='filter[movie]'),
    _free: bool | None = Query(default=None, alias='filter[is_free]'),
    _sub: bool | None = Query(default=None, alias='filter[private]'),
    _ticket: int | None = Query(default=None, alias='filter[tickets]'),
    _date: datetime | None = Query(default=None, alias='filter[date]'),
    _location: str | None = Query(default=None, alias='filter[location]'),
    announcement_service: AnnouncementService = Depends(get_announcement_service),
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> list[resp_announce.AnnouncementResponse] | list:
    query = payload_announce.MultyPayload(
        author=_author,
        movie=_movie,
        free=_free,
        sub=_sub,
        ticket=_ticket,
        date=_date,
        location=_location,
    )
    return await announcement_service.get_multy(query=query, user_id=_user.get('user_id'))


@router.delete(
    '/announcement/{announcement_id}',
    summary='Удалить свое объявление',
    description='Удаление записи из DB',
    response_description='HTTPStatus',
)
async def delete(
    announcement_id: str,
    announcement_service: AnnouncementService = Depends(get_announcement_service),
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> HTTPStatus:
    try:
        await announcement_service.delete(announce_id=announcement_id, user=_user)
        return HTTPStatus.OK
    except exc.NotFoundError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    except exc.NoAccessError:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN)


@router.get(
    '/announcement/{announcement_id}/{guest_id}',
    summary='Служебная ручка. Получить информацию для review',
    description='Получение информации для review',
    response_model=resp_announce.AnnouncementToReviewResponse,
    response_description='Получение информации для сервиса рейтинга',
)
async def get_staff(
    announcement_id: str,
    guest_id: str,
    announcement_service: AnnouncementService = Depends(get_announcement_service),
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> resp_announce.AnnouncementToReviewResponse:

    return await announcement_service.get_to_review(announce_id=announcement_id, guest_id=guest_id)
