from typing import Protocol
from uuid import UUID

from src.application.user import dto


class UserReader(Protocol):
    async def get_user_by_id(self, user_id: UUID) -> dto.UserDTOs:
        raise NotImplementedError
