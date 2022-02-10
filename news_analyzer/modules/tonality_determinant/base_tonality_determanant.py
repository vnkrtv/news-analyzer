from abc import abstractmethod, ABC
from typing import Dict

from news_analyzer.modules.tonality_determinant.schemas.sentiment_type import (
    SentimentType,
)


class BaseTonalityDeterminant(ABC):
    @abstractmethod
    def get_tonality(self, text: str) -> Dict[SentimentType, float]:
        raise NotImplementedError
