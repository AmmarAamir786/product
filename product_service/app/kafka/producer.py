from aiokafka import AIOKafkaProducer
from product_service.app.settings import BOOTSTRAP_SERVER

async def producer(topic, message):
    producer = AIOKafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER)
    await producer.start()
    try:
        await producer.send_and_wait(topic, message)
    finally:
        await producer.stop()