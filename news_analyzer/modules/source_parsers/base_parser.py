from typing import List, Any
from abc import abstractmethod, ABC


class BaseParser(ABC):

    @abstractmethod
    def parse(self, text: str):
        raise NotImplementedError
