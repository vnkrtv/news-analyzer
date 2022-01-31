from typing import List, Dict
from bs4 import BeautifulSoup

from news_analyzer.modules.source_parsers.base_parser import BaseParser


class MeduzaArticleParser(BaseParser):

    def __extract_title(self, soup: BeautifulSoup) -> str:
        text = soup.find('h1')
        return ' '.join(text.split())

    def __extract_text(self, soup: BeautifulSoup) -> str:
        texts = []
        for paragraph in soup.select("p[class^=SimpleBlock-module_p__]"):
            texts.append(' '.join(paragraph.text.split()))
        return ' '.join(texts)

    def parse(self, text: str) -> :
        soup = BeautifulSoup(text, 'html.parser')

