from typing import List, Dict
import xml.etree.ElementTree as ET

from news_analyzer.modules.parsers.base_source_parser import BaseSourceParser


class MeduzaRSSParser(BaseSourceParser):
    async def parse(self, text: str) -> List[str]:
        root = ET.fromstring(text)
        items = root[0].findall("item")
        return [
            {"title": " ".join(item[0].text.split()), "link": item[1].text}
            for item in items
        ]
