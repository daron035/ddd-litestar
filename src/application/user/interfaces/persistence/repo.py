from abc import abstractmethod
from typing import Protocol

from src.domain.user import entities
from src.domain.user.value_objects import Username


class UserRepo(Protocol):
    # @abstractmethod
    # async def acquire_user_by_id(self, user_id: UserId) -> entities.User:
    #     raise NotImplementedError

    @abstractmethod
    async def add_user(self, user: entities.User) -> None:
        raise NotImplementedError

    # @abstractmethod
    # async def update_user(self, user: entities.User) -> None:
    #     raise NotImplementedError

    @abstractmethod
    async def get_existing_usernames(self) -> set[Username]:
        raise NotImplementedError
