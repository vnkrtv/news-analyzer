from typing import List, Any
from abc import abstractmethod, ABC

from news_analyzer.modules.parsers.schemas.article_info import ArticleInfo


class BaseArticleParser(ABC):
    @abstractmethod
    async def parse(self, text: str) -> ArticleInfo:
        raise NotImplementedError
