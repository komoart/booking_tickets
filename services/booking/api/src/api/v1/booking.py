from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

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
