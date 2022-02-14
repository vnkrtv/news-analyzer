import logging
from datetime import datetime
from select import select
from typing import Any, Optional, List, Dict, Tuple

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from news_analyzer.db.manager.base_manager import BaseModelManager
from news_analyzer.db.models.named_entity import NamedEntity, InputNamedEntity
from news_analyzer.db.models.named_entity_tonality import (
    NamedEntityTonality,
    NamedEntityTonalityList,
    NamedEntityTonalityWithSourceList,
    NamedEntityTonalityWithSource,
)
from news_analyzer.db.schema import named_entities_table


class NamedEntityManager(BaseModelManager):
    date_format: str = "%Y/%m/%d %H:%M"

    def __init__(self, engine: AsyncEngine):
        super().__init__(named_entities_table, engine)

    async def all(self) -> List[NamedEntity]:
        return [NamedEntity(**data) for data in await self._all()]

    async def create(self, entity: InputNamedEntity) -> None:
        await self._create(entity.dict())

    async def bulk_create(self, entities: List[InputNamedEntity]) -> None:
        await self._bulk_create([_.dict() for _ in entities])

    async def all_by_src(self, src_id: int) -> List[NamedEntity]:
        async with self.engine.connect() as conn:
            result = await conn.execute(
                select(self.model_table).where(self.model_table.c.src_id == src_id)
            )
            return [NamedEntity(**data) for data in result.mappings().all()]

    async def group_by_name(
        self,
        src_id: Optional[int] = None,
        entity_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> NamedEntityTonalityList:
        sql, params = self._get_group_by_sql(
            group_by_src=False,
            src_id=src_id,
            entity_id=entity_id,
            start_date=start_date,
            end_date=end_date,
        )
        async with self.engine.connect() as conn:
            result = await conn.execute(sql, params)
            return NamedEntityTonalityList(
                entities=[
                    NamedEntityTonality(**data) for data in result.mappings().all()
                ],
                start_date=start_date,
                end_date=end_date,
            )

    async def group_by_name_and_src(
        self,
        src_id: int,
        entity_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> NamedEntityTonalityWithSourceList:
        sql, params = self._get_group_by_sql(
            group_by_src=True,
            src_id=src_id,
            entity_id=entity_id,
            start_date=start_date,
            end_date=end_date,
        )
        async with self.engine.connect() as conn:
            result = await conn.execute(sql, params)
            return NamedEntityTonalityWithSourceList(
                entities=[
                    NamedEntityTonalityWithSource(**data)
                    for data in result.mappings().all()
                ],
                start_date=start_date,
                end_date=end_date,
            )

    def _get_group_by_sql(
        self,
        group_by_src: bool,
        src_id: Optional[int] = None,
        entity_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Tuple[text, Dict[str, Any]]:
        where_condition, params = self._get_where_condition(
            date_col="a.date",
            src_id_col="a_s.src_id",
            entity_id_col="n_e.entity_id",
            src_id=src_id,
            entity_id=entity_id,
            start_date=start_date,
            end_date=end_date,
        )

        return (
            text(
                f"""
            SELECT
                   n_e.name                  AS "name",
                   n_e.entity_type           AS "entity_type",
                   {'a_s.name                AS "src_name",' if group_by_src else ''}
                   avg(a.neutral_sentiment)  AS "mean_neutral_sentiment",
                   avg(a.negative_sentiment) AS "mean_negative_sentiment",
                   avg(a.positive_sentiment) AS "mean_positive_sentiment",
                   avg(a.skip_sentiment)     AS "mean_skip_sentiment",
                   avg(a.speech_sentiment)   AS "mean_speech_sentiment"
            FROM named_entities n_e
            INNER JOIN articles a ON n_e.article_id = a.article_id
            INNER JOIN articles_sources a_s on a.src_id = a_s.src_id
            {where_condition if where_condition else ''}
            GROUP BY n_e.name, n_e.entity_type {', a_s.src_id' if group_by_src else ''}
        """
            ),
            params,
        )

    def _get_date_condition(
        self,
        date_col: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Tuple[Optional[str], Dict[str, Any]]:
        if not start_date and not end_date:
            return None, {}
        if start_date:
            if end_date:
                return f"{date_col} BETWEEN :start_date AND :end_date", {
                    "start_date": start_date,
                    "end_date": end_date,
                }
            return f"{date_col} > :start_date", {"start_date": start_date}
        return f"{date_col} < :end_date", {"end_date": end_date}

    def _get_where_condition(
        self,
        date_col: str,
        src_id_col: str,
        entity_id_col: str,
        src_id: Optional[int] = None,
        entity_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Tuple[Optional[str], Dict[str, Any]]:
        date_condition, params = self._get_date_condition(
            date_col, start_date, end_date
        )
        if entity_id:
            params["entity_id"] = entity_id
        if src_id:
            params["src_id"] = src_id

        where_condition = None
        if src_id:
            if date_condition:
                if entity_id:
                    where_condition = f"WHERE {src_id_col} = :src_id AND {date_condition} AND {entity_id_col} = :entity_id"
                else:
                    where_condition = (
                        f"WHERE {src_id_col} = :src_id AND {date_condition}"
                    )
            else:
                if entity_id:
                    where_condition = (
                        f"WHERE {src_id_col} AND {entity_id_col} = :entity_id"
                    )
                else:
                    where_condition = (
                        f"WHERE {src_id_col} AND {entity_id_col} = :entity_id"
                    )

        elif date_condition:
            if entity_id:
                where_condition = (
                    f"WHERE {date_condition} AND {entity_id_col} = :entity_id"
                )
            else:
                where_condition = f"WHERE {date_condition}"
        return where_condition, params
