import random
from uuid import uuid4

from faker import Faker

from models import MovieInfo, MovieType

fake = Faker()


def get_fake_movie(movie_id: str | None = None) -> MovieInfo:
    if not movie_id:
        movie_id = uuid4()

    return MovieInfo(
        id=str(movie_id),
        imdb_rating=5.5,
        genre=[MovieType.movie.value, MovieType.documentary.value],
        title='Fake movie',
        description='Fake description',
        director=fake.name(),
        actors_names=[fake.name(), fake.name()],
        writers_names=[fake.name(), fake.name()],
        duration=random.randint(45, 180),
    )
