from src.infrastructure.message_broker.factories import KafkaConnectionFactory
from src.infrastructure.message_broker.interface import MessageBroker


class KafkaMessageBroker(KafkaConnectionFactory, MessageBroker):
    async def publish_message(self, topic: str, key: bytes, value: bytes) -> None:
        await self.producer.send(topic=topic, key=key, value=value)
