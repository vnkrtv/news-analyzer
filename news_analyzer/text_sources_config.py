from news_analyzer import text_sources
from news_analyzer.modules.loader.web_loader import WebLoader
from news_analyzer.modules.ner_extractor.natasha_ner_extractor import (
    NatashaNerExtractor,
)
from news_analyzer.modules.tonality_determinant.dostoevsky_tonality_determinant import (
    DostoevskyTonalityDeterminant,
)

TEXT_SOURCES_CONFIG = {
    "meduza": {
        "source_loader": WebLoader,
        "source_parser": text_sources.meduza.MeduzaRSSParser,
        "text_loader": WebLoader,
        "text_parser": text_sources.meduza.MeduzaArticleParser,
        "ner_extractor": NatashaNerExtractor,
        "tonality_determinant": DostoevskyTonalityDeterminant,
    }
}
