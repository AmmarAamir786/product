from aiokafka import AIOKafkaProducer
from app.settings import BOOTSTRAP_SERVER

async def producer() -> AIOKafkaProducer:
    producer = AIOKafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER)
    await producer.start()
    try:
        yield producer  # Provide producer instance to the calling route
    finally:
        await producer.stop()
