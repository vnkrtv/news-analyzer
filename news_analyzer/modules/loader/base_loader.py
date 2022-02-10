from abc import abstractmethod, ABC


class BaseLoader(ABC):
    @abstractmethod
    async def load(self, src: str) -> str:
        raise NotImplementedError
