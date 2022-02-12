import logging

from news_analyzer.db.db_manager import DBManager
from news_analyzer.db.models.article import Article, InputArticle
from news_analyzer.db.models.named_entity import NamedEntity, InputNamedEntity
from news_analyzer.errors.task_processing_errors import SourceNotFoundError
from news_analyzer.modules.articles_getter.articles_getter import ArticlesGetter
from news_analyzer.modules.task_processor.schemas.load_text_task_description import (
    LoadTextTaskDescription,
)
from news_analyzer.modules.task_processor.schemas.task import Task
from news_analyzer.modules.task_processor.schemas.task_type import TaskType
from news_analyzer.modules.text_analyzer.text_analyzer import TextAnalyzer
from news_analyzer.modules.tonality_determinant.schemas.sentiment_type import (
    SentimentType,
)


class TaskProcessor:
    def __init__(self, db: DBManager):
        self.db = db

    async def process(self, task: Task) -> None:
        if task.type == TaskType.LOAD_TEXT:
            await self.__process_load_text_task(
                LoadTextTaskDescription(**task.description)
            )

    async def __process_load_text_task(
        self, description: LoadTextTaskDescription
    ) -> None:
        src_name, src, src_id = (
            description.src_name,
            description.src,
            description.src_id,
        )

        try:
            articles_getter = ArticlesGetter.get_for_src(
                src_name=src_name, src=src, timeout=description.timeout
            )
            text_analyzer = TextAnalyzer.get_for_src(src_name=src_name)
        except SourceNotFoundError as e:
            logging.error(e)
            return

        articles = await articles_getter.get_articles()
        logging.info("load %d articles from '%s'", len(articles), src_name)

        for loaded_article in articles:
            article_info = loaded_article.article_info
            text_analysis_info = await text_analyzer.analyze(text=article_info.text)

            article = InputArticle(
                src_id=src_id,
                title=article_info.title,
                text=article_info.text,
                date=article_info.date,
                neutral_sentiment=text_analysis_info.sentiment.get(
                    SentimentType.NEUTRAL
                ),
                negative_sentiment=text_analysis_info.sentiment.get(
                    SentimentType.NEGATIVE
                ),
                positive_sentiment=text_analysis_info.sentiment.get(
                    SentimentType.POSITIVE
                ),
                skip_sentiment=text_analysis_info.sentiment.get(SentimentType.SKIP),
                speech_sentiment=text_analysis_info.sentiment.get(SentimentType.SPEECH),
            )
            article = await self.db.articles.create_and_return(article)
            logging.info("load article '%s' from '%s' to db", article.title, src_name)

            entities = []
            for entity in text_analysis_info.entities:
                entities.append(
                    InputNamedEntity(
                        article_id=article.article_id,
                        name=entity.text,
                        entity_type=entity.type,
                    )
                )

            await self.db.named_entities.bulk_create(entities)
            logging.info(
                "load %d entities from article '%s' from '%s' to db",
                len(entities),
                article.title,
                src_name,
            )
