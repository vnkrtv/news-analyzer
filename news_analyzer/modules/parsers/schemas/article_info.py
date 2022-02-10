from datetime import datetime

from news_analyzer.modules.base_schema import BaseSchema


class ArticleInfo(BaseSchema):
    text: str
    title: str
    date: datetime
