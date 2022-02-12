from datetime import datetime
from typing import List, Dict
from bs4 import BeautifulSoup

from news_analyzer.modules.parsers.base_article_parser import BaseArticleParser
from news_analyzer.modules.parsers.schemas.article_info import ArticleInfo


class MeduzaArticleParser(BaseArticleParser):
    ru_month_to_en = {
        "января": "Jan",
        "февраля": "Feb",
        "марта": "Mar",
        "апреля": "Apr",
        "мая": "May",
        "июня": "Jun",
        "июля": "Jul",
        "августа": "Aug",
        "октября": "Oct",
        "ноября": "Nov",
        "декабря": "Dec",
    }

    def __extract_title(self, soup: BeautifulSoup) -> str:
        text = soup.find("h1").text
        return " ".join(text.split())

    def __extract_text(self, soup: BeautifulSoup) -> str:
        texts = []
        for paragraph in soup.select("p[class^=SimpleBlock-module_p__]"):
            texts.append(" ".join(paragraph.text.split()))
        return " ".join(texts)

    def __extract_date(self, soup: BeautifulSoup) -> datetime:
        """
        Parse date of format '20:42, 12 февраля 2022' to datetime
        """
        date_str = soup.find("time").text
        month = date_str.split(" ")[2]

        return datetime.strptime(
            date_str.replace(month, self.ru_month_to_en[month]), "%H:%M, %d %b %Y"
        )

    async def parse(self, text: str) -> ArticleInfo:
        soup = BeautifulSoup(text, "html.parser")
        return ArticleInfo(
            text=self.__extract_text(soup),
            title=self.__extract_title(soup),
            date=self.__extract_date(soup),
        )
