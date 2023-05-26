from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query

import utils.exceptions as exc
from api.v1.components import payload_booking, resp_booking
from services.booking.service.booking import BookingService, get_booking_service
from utils import auth

router = APIRouter()
auth_handler = auth.AuthHandler()


@router.post(
    '/booking/{announcement_id}',
    summary='Создать заявку',
    description='Создание записи в DB',
    response_model=resp_booking.DetailBookingResponse,
    response_description='Подробная информация из заявки',
)
async def create(
    announcement_id: str,
    booking_service: BookingService = Depends(get_booking_service),
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> resp_booking.DetailBookingResponse:
    try:
        return await booking_service.create(announce_id=announcement_id, user=_user)
    except exc.UniqueConstraintError:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
    except exc.NoAccessError:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN)


@router.put(
    '/booking/{booking_id}',
    summary='Изменить свой статус в заявке',
    description='Изменение записи в DB',
    response_model=resp_booking.DetailBookingResponse,
    response_description='Подробная информация после изменения',
)
async def update(
    booking_id: str,
    payload: payload_booking.UpdatePayload,
    booking_service: BookingService = Depends(get_booking_service),
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> resp_booking.DetailBookingResponse:
    try:
        await booking_service.update(
            user=_user,
            booking_id=booking_id,
            new_status=payload,
        )
    except exc.NotFoundError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    except exc.UniqueConstraintError:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
    except exc.NoAccessError:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN)
    return await booking_service.get_one(booking_id=booking_id, user=_user)


@router.get(
    '/booking/{booking_id}',
    summary='Получить заявку по id',
    description='Получение всей информации по заявке, сервис идет за информацией в db, Auth, Movie_api',
    response_model=resp_booking.DetailBookingResponse,
    response_description='Подробная информация из объявления',
)
async def get_one(
    booking_id: str,
    booking_service: BookingService = Depends(get_booking_service),
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> resp_booking.DetailBookingResponse:
    try:
        return await booking_service.get_one(booking_id=booking_id, user=_user)
    except exc.NotFoundError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    except exc.NoAccessError:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN)


@router.get(
    '/bookings',
    summary='Получить список всех своих заявок',
    description='Получение списка заявок, сервис идет за информацией в db',
    response_model=list[resp_booking.BookingResponse],
    response_description='Список объявлений по условию',
)
async def get_multy(
    _role: payload_booking.Role | None = Query(default=payload_booking.Role.author, alias='filter[self]'),
    _movie: str | None = Query(default=None, alias='filter[movie]'),
    _date: datetime | None = Query(default=None, alias='filter[date]'),
    booking_service: BookingService = Depends(get_booking_service),
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> list[resp_booking.BookingResponse]:
    query = payload_booking.MultyPayload(
        role=_role,
        movie=_movie,
        date=_date,
    )
    try:
        return await booking_service.get_multy(user=_user, query=query)
    except exc.ValueMissingError:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY)


@router.get(
    '/_bookings',
    summary='Служебный метод. Получить список всех заявок',
    description='Получение списка объявлений, сервис идет за информацией в db',
    response_model=list[resp_booking.BookingResponse],
    response_description='Список объявлений по условию',
)
async def sudo_get_multy(
    _author: str | None = Query(default=None, alias='filter[author]'),
    _movie: str | None = Query(default=None, alias='filter[movie]'),
    _date: datetime | None = Query(default=None, alias='filter[date]'),
    booking_service: BookingService = Depends(get_booking_service),
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> list[resp_booking.BookingResponse]:
    if _user.get('claims').get('is_super'):
        query = payload_booking.SudoMultyPayload(
            author=_author,
            movie=_movie,
            date=_date,
        )
        return await booking_service.sudo_get_multy(user=_user, query=query)
    raise HTTPException(status_code=HTTPStatus.FORBIDDEN)


@router.delete(
    '/booking/{booking_id}',
    summary='Удалить заявку',
    description='Удаление записи из DB',
    response_description='HTTPStatus',
)
async def delete(
    booking_id: str,
    booking_service: BookingService = Depends(get_booking_service),
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> HTTPStatus:
    try:
        await booking_service.delete(user=_user, booking_id=booking_id)
        return HTTPStatus.OK
    except exc.NotFoundError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    except exc.NoAccessError:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN)
