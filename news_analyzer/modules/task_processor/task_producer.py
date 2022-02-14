import time
from typing import List

from sqlalchemy.ext.asyncio import create_async_engine

from news_analyzer.db.db_manager import DBManager
from news_analyzer.db.models.articles_source import ArticlesSource, InputArticlesSource
from news_analyzer.db.schema import TextSourceType
from news_analyzer.modules.task_processor.schemas.load_text_task_description import (
    LoadTextTaskDescription,
)
from news_analyzer.modules.task_processor.schemas.task import Task
from news_analyzer.modules.task_processor.schemas.task_type import TaskType
from news_analyzer.modules.task_processor.task_processor import TaskProcessor
from news_analyzer.settings import Config
from news_analyzer.text_sources_config import TEXT_SOURCES_CONFIG


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


def get_sources_from_config() -> List[InputArticlesSource]:
    return [
        InputArticlesSource(
            name=src_name,
            src_type=src_config["info"]["src_type"],
            src=src_config["info"]["src"],
        )
        for src_name, src_config in TEXT_SOURCES_CONFIG.items()
    ]


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

    for src in get_sources_from_config():
        try:
            await db.articles_sources.create(src)
        except:
            # we can use upsert statement to avoid errors on duplicate key
            # but in that case we have to write an implementation tied to a specific DBMS
            pass

    while True:
        for source in await db.articles_sources.all():
            task = Task(
                type=get_task_type(source.src_type),
                description=get_task_description(source),
            )
            await task_processor.process(task)

        time.sleep(Config.TaskProducer.interval)
