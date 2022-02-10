from news_analyzer.db.db_manager import DBManager
from news_analyzer.db.models.article import Article, InputArticle
from news_analyzer.db.models.named_entity import NamedEntity, InputNamedEntity
from news_analyzer.modules.articles_getter.articles_getter import ArticlesGetter
from news_analyzer.modules.task_consumer.schemas.task import Task
from news_analyzer.modules.task_consumer.schemas.task_type import TaskType
from news_analyzer.modules.text_analyzer.text_analyzer import TextAnalyzer
from news_analyzer.modules.tonality_determinant.schemas.sentiment_type import SentimentType


class TaskProcessor:

    def __init__(self, db_manager: DBManager):
        self.db = db_manager

    async def process(self, task: Task) -> None:
        if task.type == TaskType.LOAD_TEXT:
            await self.__process_load_text_task(task.description)

    async def __process_load_text_task(self, description: dict) -> None:
        try:
            articles_getter = ArticlesGetter.get_for_src(src=description['src'])
            text_analyzer = TextAnalyzer.get_for_src(src=description['src'])
        except:
            return

        for loaded_article in await articles_getter.get_articles():
            article_info = loaded_article.article_info
            text_analysis_info = await text_analyzer.analyze(text=article_info.text)

            article = InputArticle(
                src_id=description['src_id'],
                title=article_info.title,
                text=article_info.text,
                date=article_info.date,
                neutral_sentiment=text_analysis_info.sentiment.get(SentimentType.NEUTRAL),
                negative_sentiment=text_analysis_info.sentiment.get(SentimentType.NEGATIVE),
                positive_sentiment=text_analysis_info.sentiment.get(SentimentType.POSITIVE),
                skip_sentiment=text_analysis_info.sentiment.get(SentimentType.SKIP),
                speech_sentiment=text_analysis_info.sentiment.get(SentimentType.SPEECH)
            )
            article = await self.db.articles.create_and_return(article)

            for entity in text_analysis_info.entities:
                await self.db.named_entities.create(
                    InputNamedEntity(
                        article_id=article.article_id,
                        name=entity.text,
                        entity_type=entity.type
                    )
                )
