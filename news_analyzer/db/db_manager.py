import time

from sqlalchemy.ext.asyncio import AsyncEngine

from news_analyzer.db.manager.article_manager import ArticleManager
from news_analyzer.db.manager.articles_source_manager import ArticlesSourceManager
from news_analyzer.db.manager.named_entity_manager import NamedEntityManager


class DBManager:
    engine: AsyncEngine

    def __init__(self, engine: AsyncEngine):
        self.engine = engine

    @property
    def articles_sources(self) -> ArticlesSourceManager:
        return ArticlesSourceManager(engine=self.engine)

    @property
    def articles(self) -> ArticleManager:
        return ArticleManager(engine=self.engine)

    @property
    def named_entities(self) -> NamedEntityManager:
        return NamedEntityManager(engine=self.engine)
