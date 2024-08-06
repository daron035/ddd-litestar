from dataclasses import dataclass

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer


@dataclass(eq=False, order=False, repr=False)
class KafkaConnectionFactory:
    producer: AIOKafkaProducer
    consumer: AIOKafkaConsumer

    async def start(self) -> None:
        await self.producer.start()
        await self.consumer.start()

    async def stop(self) -> None:
        await self.producer.stop()
        await self.consumer.stop()
