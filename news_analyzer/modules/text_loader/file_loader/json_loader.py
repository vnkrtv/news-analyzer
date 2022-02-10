import json
from typing import List

from news_analyzer.modules.text_loader.file_loader.file_loader import FileLoader


class JsonLoader(FileLoader):
    async def read_file(self, file_name: str) -> List[str]:
        with open(file_name, "r") as f:
            return json.load(f)
