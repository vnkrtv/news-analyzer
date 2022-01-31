from typing import List

from news_analyzer.modules.text_loader.base_loader import BaseLoader


class WebLoader(BaseLoader):

    async def load(self, src: str) -> List[str]:
        raise NotImplementedError
