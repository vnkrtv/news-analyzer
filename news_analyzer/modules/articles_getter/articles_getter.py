import time
from typing import List, Optional

from news_analyzer.errors.task_processing_errors import SourceNotFoundError
from news_analyzer.modules.articles_getter.schemas.loaded_article import LoadedArticle
from news_analyzer.modules.loader.base_loader import BaseLoader
from news_analyzer.modules.parsers.base_article_parser import BaseArticleParser
from news_analyzer.modules.parsers.base_source_parser import BaseSourceParser
from news_analyzer.text_sources_config import TEXT_SOURCES_CONFIG


class ArticlesGetter:
    def __init__(
        self,
        src: str,
        source_loader: BaseLoader,
        source_parser: BaseSourceParser,
        text_loader: BaseLoader,
        text_parser: BaseArticleParser,
        **kwargs,
    ):
        self.src = src

        self.source_loader = source_loader
        self.source_parser = source_parser
        self.text_loader = text_loader
        self.text_parser = text_parser

        self.timeout = kwargs.get("timeout")

    @classmethod
    def get_for_src(cls, src_name: str, src: str, **kwargs):
        text_src_config = TEXT_SOURCES_CONFIG.get(src_name)
        if not text_src_config:
            raise SourceNotFoundError(
                f'src "{src_name}" not found in TEXT_SOURCES_CONFIG'
            )

        return cls(
            src=src,
            source_loader=text_src_config.get("source_loader")(),
            source_parser=text_src_config.get("source_parser")(),
            text_loader=text_src_config.get("text_loader")(),
            text_parser=text_src_config.get("text_parser")(),
            **kwargs,
        )

    async def get_articles(self) -> List[LoadedArticle]:
        sources_content = await self.source_loader.load(src=self.src)
        sources = await self.source_parser.parse(sources_content)

        loaded_texts = []
        for src in sources:
            content = await self.text_loader.load(src=src)
            article_info = await self.text_parser.parse(content)
            loaded_texts.append(
                LoadedArticle(
                    article_info=article_info,
                    src=src,
                )
            )

            if self.timeout:
                time.sleep(self.timeout)

        return loaded_texts
