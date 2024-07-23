from collections.abc import Mapping
from typing import Any

from src.domain.common import value_objects as gvo
from src.domain.messages.entities import Chat
from src.domain.messages.entities.messages import Message


def convert_chat_entity_to_document(chat: Chat) -> dict:
    return {
        "id": str(chat.id.to_raw()),
        "title": chat.title.to_raw(),
        "created_at": chat.created_at,
    }


def convert_chat_document_to_entity(chat_document: Mapping[str, Any]) -> Chat:
    return Chat(
        id=gvo.Id(chat_document["id"]),
        title=chat_document["title"],
        created_at=chat_document["created_at"],
    )


def convert_message_entity_to_document(message: Message) -> dict:
    return {
        "id": str(message.id.to_raw()),
        "text": str(message.text.to_raw()),
        "chat_id": str(message.chat_id.to_raw()),
        "created_at": message.created_at,
    }
