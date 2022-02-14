from datetime import datetime

from news_analyzer.modules.base_schema import BaseSchema


class InputArticle(BaseSchema):
    src_id: int
    title: str
    text: str
    date: datetime
    neutral_sentiment: float
    negative_sentiment: float
    positive_sentiment: float
    skip_sentiment: float
    speech_sentiment: float


class Article(InputArticle):
    article_id: int
