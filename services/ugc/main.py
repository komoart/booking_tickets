from random import randint

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from config import settings
from utils import get_fake_group, get_fake_review_info

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/ugc/api/openapi',
    openapi_url='/ugc/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.post('/ugc/v1/review_info/{movie_id}/{user_id}/{review_id}')
async def review_info(movie_id: str, user_id: str, review_id: str):
    return get_fake_review_info(movie_id, user_id, review_id)


@app.post('/ugc/v1/subscribers/{movie_id}')
async def subscribers_group(movie_id: str):
    return get_fake_group()


@app.post('/ugc/v1/likes_count/{review_id}')
async def likes_count_info(review_id: str):
    return {'likes_count': randint(1, 20)}


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8082)
