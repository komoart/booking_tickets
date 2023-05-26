from enum import Enum
from pathlib import Path
from random import choice
from string import ascii_letters

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = Path(Path(__file__).parent.parent.parent.parent.parent.parent, 'env')
        env_file_encoding = 'utf-8'


class LoggingSettings(BaseConfig):
    SENTRY_DSN: str = ''
    LOGSTASH_HOST: str = 'logstash'
    LOGSTASH_PORT: int = 5044

    class Config:
        env_prefix = 'LOGGING_'


class DebugSettings(BaseConfig):
    DEBUG: bool = True

    class Config:
        env_prefix = 'DEBUG_'


class PostgresSettings(BaseConfig):
    DB: str = 'db_name'
    USER: str = 'guest'
    PASSWORD: str = 'guest'
    HOST: str = 'localhost'
    PORT: int = 5432

    @property
    def uri(self):
        return f'postgresql+psycopg2://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}'

    @property
    def a_uri(self):
        return f'postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}'

    class Config:
        env_prefix = 'POSTGRES_'


class FastapiSetting(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8080
    API_PREFIX: str = '/app/v1'

    class Config:
        env_prefix = 'FASTAPI_'


class AuthMock(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8081
    PREFIX: str = '/auth/v1/'

    @property
    def uri(self):
        return f'http://{self.HOST}:{self.PORT}{self.PREFIX}'

    class Config:
        env_prefix = 'AUTH_API_'


class MovieAPIMock(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8083
    PREFIX: str = '/movie/v1/'

    @property
    def uri(self):
        return f'http://{self.HOST}:{self.PORT}{self.PREFIX}'

    class Config:
        env_prefix = 'MOVIE_API_'


class UGCMock(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8082
    PREFIX: str = '/ugc/v1/'

    @property
    def uri(self):
        return f'http://{self.HOST}:{self.PORT}{self.PREFIX}'

    class Config:
        env_prefix = 'UGC_API_'


class PermissionSettings(Enum):
    User = 0
    Subscriber = 1
    Vip_subscriber = 2
    Moderator = 3


class JWTSettings(BaseConfig):
    SECRET_KEY: str = ''.join(choice(ascii_letters) for _ in range(200))
    JWT_TOKEN_LOCATION: list = ['headers']
    ALGORITHM: str = 'HS256'

    class Config:
        env_prefix = 'JWT_'


class RedisSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 6379
    INDEX: int = 0
    EXPIRE_SEC: int = 5 * 60  # 5 minutes

    @property
    def uri(self):
        return f'redis://{self.HOST}:{self.PORT}/{self.INDEX}'

    class Config:
        env_prefix = 'REDIS_'


class URLShortnerSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 3000
    PREFIX: str = '/api/v1/shortener/'
    DEBUG: bool = True
    TESTING: bool = True
    ID_LENGTH: int = 8
    REDIRECT_URL: str = ''

    @property
    def uri(self):
        return f'http://{self.HOST}:{self.PORT}{self.PREFIX}'

    class Config:
        env_prefix = 'URLSHORT_'


class NotificationSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8070
    NOTIFIC_PREFIX: str = '/app/v1/notification/'

    @property
    def uri(self):
        return f'http://{self.HOST}:{self.PORT}{self.NOTIFIC_PREFIX}'

    class Config:
        env_prefix = 'NOTIFIC_FASTAPI_'


class RatingSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8084
    RATING_PREFIX: str = '/app/v1/average_score/'

    @property
    def uri(self):
        return f'http://{self.HOST}:{self.PORT}{self.RATING_PREFIX}'

    class Config:
        env_prefix = 'REVIEW_API'


class ProjectSettings(BaseConfig):
    PROJECT_NAME: str = 'Graduate_work'
    BASE_DIR = Path(__file__).parent.parent
    logging: LoggingSettings = LoggingSettings()
    debug: DebugSettings = DebugSettings()
    postgres: PostgresSettings = PostgresSettings()
    fastapi: FastapiSetting = FastapiSetting()
    jwt: JWTSettings = JWTSettings()
    auth: AuthMock = AuthMock()
    movie_api: MovieAPIMock = MovieAPIMock()
    ugc: UGCMock = UGCMock()
    url_shortner: URLShortnerSettings = URLShortnerSettings()
    nptific: NotificationSettings = NotificationSettings()
    redis: RedisSettings = RedisSettings()
    permission = PermissionSettings
    rating: RatingSettings = RatingSettings()


settings = ProjectSettings()
