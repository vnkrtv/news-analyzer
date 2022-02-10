from news_analyzer.modules.base_schema import BaseSchema
from news_analyzer.modules.parsers.schemas.article_info import ArticleInfo


class LoadedArticle(BaseSchema):
    article_info: ArticleInfo
    src: str
