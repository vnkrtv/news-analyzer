from typing import List, Dict
from bs4 import BeautifulSoup

from news_analyzer.modules.parsers.base_article_parser import BaseArticleParser
from news_analyzer.modules.parsers.schemas.article_info import ArticleInfo


class MeduzaArticleParser(BaseArticleParser):
    def __extract_title(self, soup: BeautifulSoup) -> str:
        text = soup.find("h1")
        return " ".join(text.split())

    def __extract_text(self, soup: BeautifulSoup) -> str:
        texts = []
        for paragraph in soup.select("p[class^=SimpleBlock-module_p__]"):
            texts.append(" ".join(paragraph.text.split()))
        return " ".join(texts)

    def parse(self, text: str) -> ArticleInfo:
        soup = BeautifulSoup(text, 'html.parser')
        return ArticleInfo()
