from news_analyzer.db.schema import TextSourceType
from news_analyzer.modules.base_schema import BaseSchema


class ArticlesSource(BaseSchema):
    src_id: int
    src_type: TextSourceType
    src: str
