from typing import Any, Optional, List

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from news_analyzer.db.manager.base_manager import BaseModelManager
from news_analyzer.db.models.named_entity import NamedEntity, InputNamedEntity
from news_analyzer.db.schema import named_entities_table


class NamedEntityManager(BaseModelManager):
    def __init__(self, engine: AsyncEngine):
        super().__init__(named_entities_table, engine)

    async def all(self) -> List[NamedEntity]:
        return [NamedEntity(**data) for data in await self.__all()]

    async def create(self, entity: InputNamedEntity) -> None:
        await self.__create(entity.dict())

    async def bulk_create(self, entities: List[InputNamedEntity]) -> None:
        await self.__bulk_create([_.dict() for _ in entities])
