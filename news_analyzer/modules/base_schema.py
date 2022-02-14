import json

from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        json_loads = json.loads
        json_dumps = json.dumps
