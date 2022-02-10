from typing import List, Any
from abc import abstractmethod, ABC


class BaseTextProcessor(ABC):
    @abstractmethod
    async def tokenize(self, text: str) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    async def sentenize(self, text: str) -> List[str]:
        raise NotImplementedError
