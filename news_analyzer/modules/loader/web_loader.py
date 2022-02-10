from typing import List, Any

from news_analyzer.modules.loader.base_loader import BaseLoader


class WebLoader(BaseLoader):

    async def load(self, src: str) -> str:
        raise NotImplementedError
