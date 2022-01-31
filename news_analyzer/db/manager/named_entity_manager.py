from typing import Any, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from news_analyzer.db.manager.base_manager import BaseModelManager
from news_analyzer.db.schema import named_entities_table


class NamedEntityManager(BaseModelManager):
    def __init__(self, engine: AsyncEngine):
        super().__init__(named_entities_table, engine)
