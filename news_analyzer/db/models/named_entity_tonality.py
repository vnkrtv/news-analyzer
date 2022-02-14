from datetime import datetime
from typing import Optional, List, Union

from news_analyzer.modules.base_schema import BaseSchema
from news_analyzer.modules.ner_extractor.schemas.ner_type import NERType


class NamedEntityTonality(BaseSchema):
    name: str
    entity_type: NERType

    mean_neutral_sentiment: float
    mean_negative_sentiment: float
    mean_positive_sentiment: float
    mean_skip_sentiment: float
    mean_speech_sentiment: float

    count: int


class NamedEntityTonalityWithSource(NamedEntityTonality):
    src_name: str


class NamedEntityTonalityList(BaseSchema):
    entities: List[NamedEntityTonality]

    start_date: Optional[datetime]
    end_date: Optional[datetime]


class NamedEntityTonalityWithSourceList(BaseSchema):
    entities: List[NamedEntityTonalityWithSource]

    start_date: Optional[datetime]
    end_date: Optional[datetime]
