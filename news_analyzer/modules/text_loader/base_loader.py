from typing import List, Any
from abc import abstractmethod, ABC


class BaseTextLoader(ABC):
    @abstractmethod
    async def load_text(self, src: str) -> str:
        raise NotImplementedError
