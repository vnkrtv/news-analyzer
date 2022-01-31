from typing import List, Any
from abc import abstractmethod, ABC

from news_analyzer.modules.ner_extractor.schemas.named_entity import NamedEntity


class BaseNerExtractor(ABC):

    @abstractmethod
    def extract(self, text: str) -> List[NamedEntity]:
        raise NotImplementedError
