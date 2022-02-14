from news_analyzer.db.schema import TextSourceType
from news_analyzer.modules.base_schema import BaseSchema


class InputArticlesSource(BaseSchema):
    name: str
    src_type: TextSourceType
    src: str


class ArticlesSource(InputArticlesSource):
    src_id: int
