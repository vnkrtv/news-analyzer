from typing import Optional, List

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from news_analyzer.db.models.articles_source import ArticlesSource
from news_analyzer.db.schema import articles_sources_table
from news_analyzer.db.manager.base_manager import BaseModelManager


class ArticlesSourceManager(BaseModelManager):
    def __init__(self, engine: AsyncEngine):
        super().__init__(articles_sources_table, engine)

    async def all(self) -> List[ArticlesSource]:
        return [ArticlesSource(**data) for data in await self._all()]
