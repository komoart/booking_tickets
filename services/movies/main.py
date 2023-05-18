import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from config import settings
from utils import get_fake_movie

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/movie/api/openapi',
    openapi_url='/movie/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.post('/movie/v1/movie/{uuid}')
async def user_info(uuid: str):
    return get_fake_movie(uuid)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8083)
