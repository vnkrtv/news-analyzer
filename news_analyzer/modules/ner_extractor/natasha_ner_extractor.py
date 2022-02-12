from typing import List, Dict, Optional

from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    NamesExtractor,
    PER,
    Doc,
)
from natasha.doc import DocSpan

from news_analyzer.modules.ner_extractor.base_ner_extractor import BaseNerExtractor
from news_analyzer.modules.ner_extractor.schemas.named_entity import NamedEntity


class NatashaNerExtractor(BaseNerExtractor):

    morph_vocab: MorphVocab = MorphVocab()
    emb: NewsEmbedding = NewsEmbedding()
    segmenter: Segmenter = Segmenter()
    ner_tagger: NewsNERTagger = NewsNERTagger(emb)
    morph_tagger: NewsMorphTagger = NewsMorphTagger(emb)
    syntax_parser: NewsSyntaxParser = NewsSyntaxParser(emb)
    names_extractor: NamesExtractor = NamesExtractor(morph_vocab)

    def __preprocess_text(self, text: str) -> Doc:
        doc = Doc(text)

        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)
        doc.parse_syntax(self.syntax_parser)

        doc.tag_ner(self.ner_tagger)
        return doc

    def __normalize(self, doc: Doc) -> None:
        for span in doc.spans:
            span.normalize(self.morph_vocab)
            if span.type == PER:
                span.extract_fact(self.names_extractor)

    @staticmethod
    def __extract_entity(span: DocSpan) -> Optional[NamedEntity]:
        if span.type != PER:
            return (
                NamedEntity(text=span.normal, type=span.type)
                if span.normal and span.type
                else None
            )
        if not span.fact:
            return None
        facts = span.fact.as_dict
        if "last" not in facts:
            return None
        if "first" in facts:
            person = f"{facts['first']} {facts['last']}"
        else:
            person = facts["last"]
        return NamedEntity(text=person, type=span.type)

    def extract(self, text: str) -> List[NamedEntity]:
        doc = self.__preprocess_text(text)
        self.__normalize(doc)

        entities = []
        for span in doc.spans:
            named_entity = self.__extract_entity(span)
            if named_entity:
                entities.append(named_entity)

        return entities
