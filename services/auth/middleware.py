from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import Response

from config import settings
from utils import parse_header


def auth_middleware(app: FastAPI):
    @app.middleware('http')
    async def check_jwt(request: Request, call_next):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return Response('Authorization header is missing', HTTPStatus.UNAUTHORIZED)
        claims = parse_header(auth_header)
        if claims.get('is_super'):
            return await call_next(request)

        user_info_path = f'{settings.fastapi.HOST}:{settings.fastapi.PORT}{settings.fastapi.PREFIX}/user_info'
        if user_info_path in str(request.url):
            if settings.permission.Moderator in claims.get('permissions'):
                return await call_next(request)
            return Response('Permission denied', HTTPStatus.FORBIDDEN)

        user_group_path = f'{settings.fastapi.HOST}:{settings.fastapi.PORT}{settings.fastapi.PREFIX}/user_group'
        if user_group_path in str(request.url):
            if settings.permission.Moderator in claims.get('permissions'):
                return await call_next(request)
            return Response('Permission denied', HTTPStatus.FORBIDDEN)
