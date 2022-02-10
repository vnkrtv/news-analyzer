from abc import abstractmethod, ABC

from news_analyzer.modules.ner_extractor.base_ner_extractor import BaseNerExtractor
from news_analyzer.modules.text_analyzer.schemas.analyzed_text import AnalyzedText
from news_analyzer.modules.tonality_determinant.base_tonality_determanant import (
    BaseTonalityDeterminant,
)


class BaseTextAnalyzer(ABC):
    def __init__(
        self,
        tonality_determinant: BaseTonalityDeterminant,
        ner_extractor: BaseNerExtractor,
    ):
        self.tonality_determinant = tonality_determinant
        self.ner_extractor = ner_extractor

    @abstractmethod
    async def analyze(self, text: str) -> AnalyzedText:
        return AnalyzedText(
            text=text,
            sentiment=self.tonality_determinant.get_tonality(text),
            entities=self.ner_extractor.extract(text),
        )
