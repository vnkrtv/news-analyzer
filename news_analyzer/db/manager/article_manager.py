from typing import Any, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from news_analyzer.db.manager.base_manager import BaseModelManager
from news_analyzer.db.schema import articles_table


class ArticleManager(BaseModelManager):
    def __init__(self, engine: AsyncEngine):
        super().__init__(articles_table, engine)
