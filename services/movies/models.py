from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class MovieType(str, Enum):
    movie = 'movie'
    series = 'series'
    cartoon = 'cartoon'
    documentary = 'documentary'

    def __repr__(self) -> str:
        return f'{self.value}'


class MovieInfo(BaseModel):
    id: str | UUID  # noqa: VNE003
    imdb_rating: float | None
    genre: list[MovieType] | None
    title: str
    description: str | None
    director: str | None
    actors_names: list[str] | None
    writers_names: list[str] | None
    duration: int

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['id'] = str(_dict['id'])
        return _dict
