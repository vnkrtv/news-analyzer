from typing import List, Any

import aiohttp

from news_analyzer.modules.loader.base_loader import BaseLoader


class WebLoader(BaseLoader):
    async def load(self, src: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(src) as resp:
                return await resp.text()
