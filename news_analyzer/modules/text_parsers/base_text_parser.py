from abc import ABC, abstractmethod


class BaseTextParser(ABC):
    @abstractmethod
    async def parse_text(self, text: str) -> str:
        raise NotImplementedError
