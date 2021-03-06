from typing import List, Dict
import xml.etree.ElementTree as ET

from news_analyzer.modules.parsers.base_source_parser import BaseSourceParser


class MeduzaRSSParser(BaseSourceParser):
    async def parse(self, text: str) -> List[str]:
        root = ET.fromstring(text)
        return [item[1].text for item in root[0].findall("item")]
