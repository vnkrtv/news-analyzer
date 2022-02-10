from typing import List, Any
from abc import abstractmethod, ABC


class BaseSourceLoader(ABC):
    @abstractmethod
    async def load_sources(self, src: str) -> List[str]:
        raise NotImplementedError
