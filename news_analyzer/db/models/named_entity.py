from news_analyzer.modules.base_schema import BaseSchema
from news_analyzer.modules.ner_extractor.schemas.ner_type import NERType


class InputNamedEntity(BaseSchema):
    article_id: int
    name: str
    entity_type: NERType


class NamedEntity(BaseSchema):
    entity_id: int
    article_id: int
    name: str
    entity_type: NERType
