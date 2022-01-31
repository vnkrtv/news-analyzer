from typing import List, Any
from abc import abstractmethod, ABC

from news_analyzer.modules.text_loader.base_loader import BaseLoader


class FileLoader(BaseLoader, ABC):

    @abstractmethod
    async def read_file(self, file_name: str) -> List[str]:
        raise NotImplementedError

    async def load(self, src: str) -> List[str]:
        return await self.read_file(src)
