from abc import ABC, abstractmethod
from typing import List

from news_analyzer.modules.source_loaders.base_source_loader import BaseSourceLoader
from news_analyzer.modules.source_parsers.base_parser import BaseSourceParser


class BaseSourceGetter(ABC):
    def __init__(self, src_loader: BaseSourceLoader, src_parser: BaseSourceParser):
        self.src_loader = src_loader
        self.src_parser = src_parser

    @abstractmethod
    async def load_sources(self, src: str) -> List[str]:
        sources = await self.src_loader.load_sources(src=src)
        return [await self.src_parser.parse(source) for source in sources]
