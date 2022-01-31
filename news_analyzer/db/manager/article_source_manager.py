from typing import Optional, List

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from news_analyzer.db.schema import article_sources_table
from news_analyzer.db.manager.base_manager import BaseModelManager


class ArticleSourceManager(BaseModelManager):
    def __init__(self, engine: AsyncEngine):
        super().__init__(article_sources_table, engine)

