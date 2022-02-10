from abc import ABC, abstractmethod

from news_analyzer.modules.text_loader.base_loader import BaseTextLoader
from news_analyzer.modules.text_parsers.base_text_parser import BaseTextParser


class BaseTextGetter(ABC):
    def __init__(self, text_loader: BaseTextLoader, text_parser: BaseTextParser):
        self.text_loader = text_loader
        self.text_parser = text_parser

    @abstractmethod
    async def load_text(self, src: str) -> str:
        text = await self.text_loader.load_text(src=src)
        return await self.text_parser.parse_text(text)
