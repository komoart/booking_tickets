from enum import Enum
from pathlib import Path
from random import choice
from string import ascii_letters

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = Path(Path(__file__).parent.parent.parent, '.env')
        env_file_encoding = 'utf-8'


class JWTSettings(BaseConfig):
    SECRET_KEY: str = ''.join(choice(ascii_letters) for _ in range(200))
    JWT_TOKEN_LOCATION: list = ['headers']
    ALGORITHM: str = 'HS256'

    class Config:
        env_prefix = 'JWT_'


class FastapiSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8081
    PREFIX: str = '/auth/v1/'

    class Config:
        env_prefix = 'AUTH_API'


class NotificSetting(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8080
    NOTIFIC_PREFIX: str = '/app/v1/notification'

    class Config:
        env_prefix = 'FASTAPI_'


class PermissionSettings(Enum):
    User = 0
    Subscriber = 1
    Vip_subscriber = 2
    Moderator = 3


class DebugSettings(BaseConfig):
    DEBUG: bool = True
    TEST_EMAIL: list[str]

    class Config:
        env_prefix = 'DEBUG_'


class ProjectSettings(BaseConfig):
    PROJECT_NAME: str = 'AUTH_API'
    BASE_DIR = Path(__file__).parent
    notific: NotificSetting = NotificSetting()
    fastapi: FastapiSettings = FastapiSettings()
    jwt: JWTSettings = JWTSettings()
    permission = PermissionSettings
    debug: DebugSettings = DebugSettings()


settings = ProjectSettings()
