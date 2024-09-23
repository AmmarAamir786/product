# main.py
from contextlib import asynccontextmanager
from typing import Annotated
from sqlmodel import Session
from fastapi import FastAPI, Depends, HTTPException
from aiokafka import AIOKafkaProducer
import asyncio
import json

from app.settings import KAFKA_PRODUCT_TOPIC
from app.models.models import Product
from app.crud.product_crud import get_all_products, get_product_by_id, delete_product_by_id, update_product_by_id
from app.db import create_tables, get_session
from app.kafka.producer import producer
from app.kafka.topic import create_topic
from app.consumers.product_consumer import consume_products
from app.utils.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Creating Tables")
    create_tables()
    logger.info("Tables Created")
    
    await create_topic(topic=KAFKA_PRODUCT_TOPIC)

    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(consume_products())
    ]

    yield

    for task in tasks:
        task.cancel()
        await task


app = FastAPI(
    lifespan=lifespan,
    title="Product Service",
    version="0.0.1",
)


@app.get("/")
def read_root():
    return {"Hello": "Product Service"}


@app.post("/products/", response_model=Product)
async def create_new_product(product: Product, producer: Annotated[AIOKafkaProducer, Depends(producer)]):
    """ Create a new product and send it to Kafka"""
    product_dict = {field: getattr(product, field) for field in product.dict()}
    product_json = json.dumps(product_dict).encode("utf-8")
    print("product_JSON:", product_json)
    
    # Produce message
    await producer.send_and_wait(KAFKA_PRODUCT_TOPIC, product_json)
    
    return product


@app.get("/products/all", response_model=list[Product])
def call_all_products(session: Annotated[Session, Depends(get_session)]):
    """ Get all products from the database"""
    return get_all_products(session)


@app.get("/products/{product_id}", response_model=Product)
def get_single_product(product_id: int, session: Annotated[Session, Depends(get_session)]):
    """ Get a single product by ID"""
    try:
        return get_product_by_id(product_id=product_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/products/{product_id}", response_model=dict)
def delete_single_product(product_id: int, session: Annotated[Session, Depends(get_session)]):
    """ Delete a single product by ID"""
    try:
        return delete_product_by_id(product_id=product_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/products/{product_id}", response_model=Product)
def update_single_product(product_id: int, product: Product, session: Annotated[Session, Depends(get_session)]):
    """ Update a single product by ID"""
    try:
        return update_product_by_id(product_id=product_id, to_update_product_data=product, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




