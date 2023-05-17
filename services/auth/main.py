import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from middleware import auth_middleware

from config import settings
from utils import create_event, get_fake_group, get_fake_user

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

if not settings.debug.DEBUG:
    auth_middleware(app)


@app.post('/auth/v1/user_info/{uuid}')
async def user_info(uuid: str):
    return get_fake_user(uuid)


@app.post('/auth/v1/user_group/{group}')
async def user_group(group: str):
    return get_fake_group()


@app.post('/auth/v1/register/')
async def welcome():
    create_event()


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8081)
