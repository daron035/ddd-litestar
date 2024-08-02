from abc import abstractmethod
from typing import Protocol

from .message import Message


class MessageBroker(Protocol):
    # @abstractmethod
    async def send_message(self, key: str, topic: str, value: bytes) -> None:
        raise NotImplementedError
    
    # async def publish_message(
    #     self,
    #     message: Message,
    #     routing_key: str,
    #     exchange_name: str,
    # ) -> None:
    #     raise NotImplementedError

    # async def declare_exchange(self, exchange_name: str) -> None:
    #     raise NotImplementedError
