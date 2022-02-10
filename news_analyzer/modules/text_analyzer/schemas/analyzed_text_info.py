from typing import Dict, List

from news_analyzer.modules.base_schema import BaseSchema
from news_analyzer.modules.ner_extractor.schemas.named_entity import NamedEntity
from news_analyzer.modules.tonality_determinant.schemas.sentiment_type import (
    SentimentType,
)


class AnalyzedTextInfo(BaseSchema):
    sentiment: Dict[SentimentType, float]
    entities: List[NamedEntity]
