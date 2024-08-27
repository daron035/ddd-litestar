from typing import TypeAlias

from src.application.common.pagination.dto import PaginatedItemsDTO

from .message import Message


MessageDTOs: TypeAlias = Message
Messages: TypeAlias = PaginatedItemsDTO[MessageDTOs]
