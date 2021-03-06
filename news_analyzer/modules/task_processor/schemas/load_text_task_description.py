from typing import Dict, List, Any, Optional

from news_analyzer.modules.base_schema import BaseSchema


class LoadTextTaskDescription(BaseSchema):
    src_name: str
    src: str
    src_id: int
    timeout: Optional[float]
