from typing import List, Any

import razdel

from news_analyzer.modules.text_processor.base_text_processor import BaseTextProcessor


class RuTextProcessor(BaseTextProcessor):
    async def tokenize(self, text: str) -> List[str]:
        return [token.text for token in razdel.tokenize(text)]

    async def sentenize(self, text: str) -> List[str]:
        return [token.text for token in razdel.sentenize(text)]
