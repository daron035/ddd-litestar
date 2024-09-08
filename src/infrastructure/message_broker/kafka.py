from collections.abc import AsyncIterator

import orjson

from src.infrastructure.message_broker.factories import KafkaConnectionFactory
from src.infrastructure.message_broker.interface import MessageBroker


class KafkaMessageBroker(KafkaConnectionFactory, MessageBroker):
    async def publish_message(
        self,
        topic: str,
        key: bytes,
        value: bytes,
        partition: int | None,
        headers: list[tuple[str, bytes]] | None,
    ) -> None:
        await self.producer.send(topic=topic, key=key, value=value, partition=partition, headers=headers)

    async def start_consuming(self, topic: str) -> AsyncIterator[dict]:
        self.consumer.subscribe(topics=[topic])

        async for event in self.consumer:
            yield orjson.loads(event.value)

    async def stop_consuming(self) -> None:
        self.consumer.unsubscribe()
