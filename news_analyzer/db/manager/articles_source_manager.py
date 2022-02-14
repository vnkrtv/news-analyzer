from typing import Optional, List

from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncEngine

from news_analyzer.db.models.articles_source import ArticlesSource
from news_analyzer.db.schema import articles_sources_table
from news_analyzer.db.manager.base_manager import BaseModelManager


class ArticlesSourceManager(BaseModelManager):
    def __init__(self, engine: AsyncEngine):
        super().__init__(articles_sources_table, engine)

    async def all(self) -> List[ArticlesSource]:
        return [ArticlesSource(**data) for data in await self._all()]

    async def all_by_type(self, src_type: str) -> List[ArticlesSource]:
        async with self.engine.connect() as conn:
            result = await conn.execute(
                select(self.model_table).where(self.model_table.c.src_type == src_type)
            )
            return [ArticlesSource(**data) for data in result.mappings().all()]
