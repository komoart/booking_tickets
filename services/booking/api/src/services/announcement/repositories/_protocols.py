from abc import ABC, abstractmethod
from uuid import UUID

from services.announcement import layer_models, layer_payload


class AnnouncementRepositoryProtocol(ABC):
    @abstractmethod
    async def get_by_id(self, announce_id: str | UUID) -> layer_models.PGAnnouncement:
        """
        :raises NotFoundError
        """
        ...

    @abstractmethod
    async def get_multy(
        self,
        query: layer_payload.APIMultyPayload,
        user: layer_models.UserToResponse,
    ) -> list[layer_models.AnnouncementResponse]:
        ...

    @abstractmethod
    async def create(
        self,
        new_announce: layer_payload.PGCreatePayload,
        movie: layer_models.MovieToResponse,
        author_id: str | UUID,
    ) -> str | UUID:
        """
        :raises UniqueConstraintError
        """
        ...

    @abstractmethod
    async def update(
        self,
        announce_id: str | UUID,
        update_announce: layer_payload.APIUpdatePayload,
    ) -> None:
        """
        :raises NotFoundError:
        :raises UniqueConstraintError
        """
        ...

    @abstractmethod
    async def delete(
        self,
        announce_id: str | UUID,
    ) -> None:
        """
        :raises NotFoundError
        """
        ...


class UserRepositoryProtocol(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: str | UUID) -> layer_models.UserToResponse:
        """
        :raises NotFoundError
        """
        ...


class BookingRepositoryProtocol(ABC):
    @abstractmethod
    async def get_by_id(self, announce_id: str | UUID) -> list[layer_models.BookingToDetailResponse]:
        ...

    @abstractmethod
    async def get_confirmed_list(self, announce_id: str | UUID) -> list[layer_models.BookingToDetailResponse]:
        ...

    @abstractmethod
    async def get_guest_id(self, announce_id: str | UUID) -> str | UUID:
        ...


class RatingRepositoryProtocol(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: str | UUID) -> layer_models.RatingToResponse:
        ...


class MovieRepositoryProtocol(ABC):
    @abstractmethod
    async def get_by_id(self, movie_id: str | UUID) -> layer_models.MovieToResponse:
        ...


class NotificRepositoryProtocol(ABC):
    @abstractmethod
    async def send(self, event_type: layer_payload.EventType, payload: layer_payload.context) -> None:
        ...
