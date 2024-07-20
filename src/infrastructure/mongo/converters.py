from src.domain.messages.entities import Chat


def convert_chat_entity_to_document(chat: Chat) -> dict:
    return {
        "id": str(chat.id.to_raw()),
        "title": chat.title.to_raw(),
    }
