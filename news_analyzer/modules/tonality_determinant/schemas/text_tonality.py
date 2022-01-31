from typing import Dict

from news_analyzer.modules.base_schema import BaseSchema
from news_analyzer.modules.tonality_determinant.schemas.sentiment_type import SentimentType


class TextTonality(BaseSchema):
    text: str
    sentiment: Dict[SentimentType, float]
