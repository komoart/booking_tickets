from datetime import date, datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class EventType(str, Enum):
    welcome = 'welcome_message'
    new_content = 'new_content'
    new_likes = 'new_likes'
    promo = 'promo'

    def __repr__(self) -> str:
        return f'{self.value}'


class DeliveryType(str, Enum):
    email = 'email'
    sms = 'sms'
    push = 'push'

    def __repr__(self) -> str:
        return f'{self.value}'


class UserInfo(BaseModel):
    user_id: str | UUID
    name: str
    last_name: str | None
    email: str | None
    phone_number: str | None
    telegram_name: str | None
    gender: str | None
    country: str | None
    time_zone: str | None
    birthday: date | None
    delivery_type: DeliveryType

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['user_id'] = str(_dict['user_id'])
        return _dict


class NewUserInfo(BaseModel):
    user_id: str | UUID
    name: str
    email: str

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['user_id'] = str(_dict['user_id'])
        return _dict


class WelcomeEvent(BaseModel):
    source_name: str
    event_type: EventType
    delivery_type: DeliveryType
    context: NewUserInfo
    created_at: datetime

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['created_at'] = _dict['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        return _dict
