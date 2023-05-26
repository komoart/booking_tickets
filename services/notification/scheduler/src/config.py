from pydantic.env_settings import BaseSettings
from pydantic.networks import PostgresDsn


class Config(BaseSettings):
    postgres_dsn: PostgresDsn = 'postgres://postgres:postgres@localhost:5432/notifications'
    publisher_chunk_size: int = 5
    select_batch_size: int = 10
    scheduler_sleep_time: int = 5
    postgres_backoff_max_time: int = 50

    user_service_url: str = 'http://127.0.0.1:8002/api/v1/'
    user_service_backoff_max_time: int = 50
    # Адрес API, принимающего события для отправки уведомлений
    notification_api_url: str = 'http://127.0.0.1:8000/api/v1/send_notification'
    notification_api_backoff_max_time: int = 50


config = Config()
