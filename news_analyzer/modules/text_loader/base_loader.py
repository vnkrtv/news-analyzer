from typing import List, Any
from abc import abstractmethod, ABC


class BaseLoader(ABC):

    @abstractmethod
    async def load(self, src: str) -> List[str]:
        raise NotImplementedError
