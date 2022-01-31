from abc import abstractmethod, ABC

from .schemas.text_tonality import TextTonality


class BaseTonalityDeterminant(ABC):

    @abstractmethod
    def get_tonality(self, text: str) -> TextTonality:
        raise NotImplementedError
