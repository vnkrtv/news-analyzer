from news_analyzer.modules.ner_extractor.base_ner_extractor import BaseNerExtractor
from news_analyzer.modules.text_analyzer.schemas.analyzed_text_info import AnalyzedTextInfo
from news_analyzer.modules.tonality_determinant.base_tonality_determanant import (
    BaseTonalityDeterminant,
)
from news_analyzer.text_sources_config import TEXT_SOURCES_CONFIG


class TextAnalyzer:

    def __init__(
        self,
        tonality_determinant: BaseTonalityDeterminant,
        ner_extractor: BaseNerExtractor,
    ):
        self.tonality_determinant = tonality_determinant
        self.ner_extractor = ner_extractor

    @classmethod
    def get_for_src(cls, src: str):
        text_src_config = TEXT_SOURCES_CONFIG.get(src)
        if not text_src_config:
            raise Exception

        return cls(
            tonality_determinant=text_src_config.get('tonality_determinant')(),
            ner_extractor=text_src_config.get('ner_extractor')()
        )

    async def analyze(self, text: str) -> AnalyzedTextInfo:
        return AnalyzedTextInfo(
            sentiment=self.tonality_determinant.get_tonality(text),
            entities=self.ner_extractor.extract(text),
        )
