from news_analyzer.modules.base_schema import BaseSchema
from news_analyzer.modules.ner_extractor.schemas.ner_type import NERType


class NamedEntity(BaseSchema):
    text: str
    type: NERType
