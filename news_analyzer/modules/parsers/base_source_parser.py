from typing import List, Any
from abc import abstractmethod, ABC


class BaseSourceParser(ABC):
    @abstractmethod
    async def parse(self, src_text: str) -> List[str]:
        raise NotImplementedError
