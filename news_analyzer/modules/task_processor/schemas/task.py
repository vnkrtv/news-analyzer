from typing import Dict, List, Any

from news_analyzer.modules.base_schema import BaseSchema
from news_analyzer.modules.task_processor.schemas.task_type import TaskType


class Task(BaseSchema):
    type: TaskType
    description: dict
