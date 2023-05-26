from http import HTTPStatus

from fastapi import APIRouter, Request

router = APIRouter()


@router.post(
    '/ping',
    summary='Test ping',
    description='Тест ping',
)
async def test_ok(request: Request) -> HTTPStatus:
    return HTTPStatus.OK
