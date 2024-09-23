import json
from app.models.models import Product
from app.crud.product_crud import add_new_product
from app.db import get_session
from app.settings import KAFKA_CONSUMER_GROUP_ID_FOR_PRODUCT, KAFKA_PRODUCT_TOPIC
from app.consumers.consumer import create_consumer
from app.utils import logger


async def consume_products():
    consumer = await create_consumer(KAFKA_PRODUCT_TOPIC, KAFKA_CONSUMER_GROUP_ID_FOR_PRODUCT)
    if not consumer:
        logger.info("Failed to create kafka product consumer")
        return
    
    try:
        async for message in consumer:
            try:
                logger.info("RAW")
                logger.info(f"Received message on topic {message.topic}")

                product_data = json.loads(message.value.decode())
                logger.info("TYPE", type(product_data))
                logger.info(f"Product Data {product_data}")

                with next(get_session()) as session:
                    logger.info("SAVING DATA TO DATABASE")
                    
                    # Attempt to insert product
                    try:
                        db_insert_product = add_new_product(
                            product_data=Product(**product_data), session=session)
                        session.commit()  # Ensure session commit
                        logger.info("DB_INSERT_PRODUCT", db_insert_product)
                    except Exception as e:
                        logger.info(f"Error inserting product into DB: {e}")
                        session.rollback()  # Rollback in case of failure
                        
            except Exception as e:
                logger.error(f"Error processing message: {e}")
    finally:
        await consumer.stop()
