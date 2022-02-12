from typing import Any, Optional, List

from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncEngine

from news_analyzer.db.manager.base_manager import BaseModelManager
from news_analyzer.db.models.article import Article, InputArticle
from news_analyzer.db.schema import articles_table


class ArticleManager(BaseModelManager):
    def __init__(self, engine: AsyncEngine):
        super().__init__(articles_table, engine)

    async def all(self) -> List[Article]:
        return [Article(**data) for data in await self._all()]

    async def create(self, article: InputArticle) -> None:
        await self._create(article.dict())

    async def create_and_return(self, article: InputArticle) -> Article:
        await self.create(article)
        return await self.get(title=article.title)

    async def get(self, title: str) -> Optional[Article]:
        async with self.engine.connect() as conn:
            result = await conn.execute(
                select(self.model_table).where(self.model_table.c.title == title)
            )
            data = result.mappings()
            return Article(**data.first()) if data else None
