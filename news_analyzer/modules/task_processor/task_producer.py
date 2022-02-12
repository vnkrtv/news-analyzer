import time

from sqlalchemy.ext.asyncio import create_async_engine

from news_analyzer.db.db_manager import DBManager
from news_analyzer.db.models.articles_source import ArticlesSource
from news_analyzer.db.schema import TextSourceType
from news_analyzer.modules.task_processor.schemas.load_text_task_description import (
    LoadTextTaskDescription,
)
from news_analyzer.modules.task_processor.schemas.task import Task
from news_analyzer.modules.task_processor.schemas.task_type import TaskType
from news_analyzer.modules.task_processor.task_processor import TaskProcessor
from news_analyzer.settings import Config


def get_task_type(src_type: TextSourceType) -> str:
    if src_type == TextSourceType.rss:
        return TaskType.LOAD_TEXT


def get_task_description(source: ArticlesSource) -> dict:
    if source.src_type == TextSourceType.rss:
        return LoadTextTaskDescription(
            src_name=source.name,
            src=source.src,
            src_id=source.src_id,
            timeout=Config.TaskProducer.timeout,
        ).dict()


async def run_task_producer():
    engine = create_async_engine(
        f"postgresql+asyncpg://{Config.DB.url}",
        pool_size=Config.DB.consumer_pool_size,
        echo=Config.Logging.DB.echo,
        echo_pool=Config.Logging.DB.echo_pool,
        hide_parameters=True,
    )

    db = DBManager(engine=engine)
    task_processor = TaskProcessor(db=db)

    while True:
        for source in await db.articles_sources.all():
            task = Task(
                type=get_task_type(source.src_type),
                description=get_task_description(source),
            )
            await task_processor.process(task)

        time.sleep(Config.TaskProducer.interval)
