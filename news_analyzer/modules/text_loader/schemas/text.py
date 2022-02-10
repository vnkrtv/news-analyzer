from news_analyzer.modules.base_schema import BaseSchema


class Text(BaseSchema):
    text: str
    src: str
