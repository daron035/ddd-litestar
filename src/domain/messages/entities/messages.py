from dataclasses import dataclass, field
from datetime import datetime

from src.domain.common.entities.aggregate_root import AggregateRoot
from src.domain.common.value_objects import Id
from src.domain.messages.events.messages import (
    ChatDeletedEvent,
    ListenerAddedEvent,
    NewChatCreatedEvent,
    NewMessageReceivedEvent,
)
from src.domain.messages.exceptions import ListenerAlreadyExistsError
from src.domain.messages.value_objects import Text, Title


@dataclass(eq=False)
class Message(AggregateRoot):
    id: Id = field(kw_only=True, default_factory=Id)
    text: Text
    chat_id: Id
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True,
    )

    @classmethod
    def create(cls, text: Text, chat_id: Id) -> "Message":
        new_message = cls(text=text, chat_id=chat_id)
        return new_message

    def __hash__(self):
        return hash(self.id)


@dataclass
class ChatListener(AggregateRoot):
    id: Id = field(init=False, kw_only=True, default_factory=Id)


@dataclass(eq=False)
class Chat(AggregateRoot):
    id: Id = field(kw_only=True, default_factory=Id)
    title: Title
    messages: set[Message] = field(default_factory=set, kw_only=True)
    listeners: set[ChatListener] = field(default_factory=set, kw_only=True)
    is_deleted: bool = field(default=False, kw_only=True)
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True,
    )

    @classmethod
    def create(cls, title: Title) -> "Chat":
        new_chat = cls(title=title)
        new_chat.record_event(NewChatCreatedEvent(chat_id=new_chat.id.to_raw(), chat_title=new_chat.title.to_raw()))
        return new_chat

    def add_message(self, message: Message) -> None:
        self.messages.add(message)
        self.record_event(
            NewMessageReceivedEvent(
                message_id=message.id.to_raw(),
                message_text=message.text.to_raw(),
                chat_id=self.id.to_raw(),
            ),
        )

    def delete(self) -> None:
        self.is_deleted = True
        self.record_event(ChatDeletedEvent(chat_id=self.id.to_raw()))

    def add_listener(self, listener: ChatListener) -> None:
        if listener in self.listeners:
            raise ListenerAlreadyExistsError(listener_id=listener.id.to_raw())

        self.listeners.add(listener)
        self.record_event(ListenerAddedEvent(listener_id=listener.id.to_raw()))
