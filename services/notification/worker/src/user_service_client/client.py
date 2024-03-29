from typing import Optional

import backoff as backoff
import requests as requests
from config import config

from .client_abstract import UserInfo, UserServiceClientAbstract


class UserServiceClient(UserServiceClientAbstract):
    @backoff.on_exception(backoff.expo, requests.exceptions.ConnectionError,
                          max_time=config.user_service_backoff_max_time)
    def get_user(self, user_id: str) -> Optional[UserInfo]:
        response = requests.get(config.user_service_url + 'user/' + user_id)
        if response.status_code == 404:
            return None
        response.raise_for_status()

        data = response.json()
        return UserInfo(**data)
