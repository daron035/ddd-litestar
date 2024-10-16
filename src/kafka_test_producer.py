import asyncio

from aiokafka import AIOKafkaProducer


async def send_one():
    producer = AIOKafkaProducer(bootstrap_servers="127.0.0.1:9092")
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        # Produce message
        await producer.send_and_wait(
            topic="test-topic",
            key=b"Yeey",
            value=b"Super-pooper message",
            headers=[("adsfasd", b"asdfsad")],
        )
    finally:
        await producer.stop()


asyncio.run(send_one())
