from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import Response

from core.config import settings
from utils.auth import parse_header


def auth_middleware(app: FastAPI):
    @app.middleware('http')
    async def check_jwt(request: Request, call_next):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return Response('Authorization header is missing', HTTPStatus.UNAUTHORIZED)
        claims = parse_header(auth_header)
        if claims.get('is_super') or settings.permission.User.value in claims.get('permissions'):
            return await call_next(request)
        return Response('Permission denied', HTTPStatus.FORBIDDEN)
