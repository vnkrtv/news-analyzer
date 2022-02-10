import asyncio
import json
import logging

import aio_pika
import aioredis
from sqlalchemy.ext.asyncio import create_async_engine

from news_analyzer.db.db_manager import DBManager
from news_analyzer.modules.task_consumer.schemas.task import Task
from news_analyzer.settings import Config


async def on_task(
    db_manager: DBManager, message: aio_pika.IncomingMessage
):
    async with message.process():
        task = Task(**json.loads(message.body))



async def listen_events(task_manager: TaskManager, engine: AsyncEngine):
    """Declare queue, message binding and start the listener."""
    loop = asyncio.get_event_loop()
    connection: aio_pika.Connection = await aio_pika.connect_robust(
        Config.RabbitMQ.url, loop=loop
    )
    logging.info("opened connection: %s", connection.url)
    try:
        channel: Channel = await connection.channel()
        await channel.set_qos(prefetch_count=100)

        tasks_exchange = await channel.get_exchange(Config.RabbitMQ.tasks_exchange_name)
        queue = await channel.declare_queue(
            name=Config.RabbitMQ.queue_name, durable=True
        )
        await queue.bind(tasks_exchange, routing_key=Config.RabbitMQ.tasks_routing_key)
        logging.info("bind to exchange: %s", Config.RabbitMQ.tasks_exchange_name)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                logging.info("get message: %s", message.body)
                await on_task(task_manager, engine, message)
    except asyncio.CancelledError:
        pass


async def run_consumer():
    engine = create_async_engine(
        f"postgresql+asyncpg://{Config.DB.url}",
        pool_size=Config.DB.consumer_pool_size,
        echo=Config.Logging.DB.echo,
        echo_pool=Config.Logging.DB.echo_pool,
        hide_parameters=True,
    )
    redis = await aioredis.create_redis_pool(
        address=Config.Redis.url,
        db=Config.Redis.db,
        password=Config.Redis.password,
        maxsize=Config.Redis.pool_maxsize,
    )
    db_manager = DBManager(engine=engine)
    logging.info("created consumer")
    await listen_events(db_manager)
