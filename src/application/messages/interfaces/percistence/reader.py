from abc import abstractmethod
from collections.abc import Iterable
from typing import Protocol
from uuid import UUID

from src.application.common.pagination.dto import Pagination
from src.application.messages.dto import Message as MessageDTO
from src.application.messages import dto

class MessageReader(Protocol):
    @abstractmethod
    async def get_messages_by_chat_id(
        self,
        chat_id: UUID,
        pagination: Pagination
    ) -> dto.Messages:
        raise NotImplementedError
