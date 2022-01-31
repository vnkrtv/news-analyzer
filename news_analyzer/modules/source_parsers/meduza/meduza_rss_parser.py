from typing import List, Dict
import xml.etree.ElementTree as ET

from news_analyzer.modules.source_parsers.base_parser import BaseParser


class MeduzaRSSParser(BaseParser):

    def parse(self, text: str) -> List[Dict[str, str]]:
        root = ET.fromstring(text)
        items = root[0].findall('item')
        return [
            {
                'title': ' '.join(item[0].text.split()),
                'link': item[1].text
            }
            for item in items
        ]
