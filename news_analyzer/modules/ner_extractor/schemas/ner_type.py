from enum import Enum


class NERType(str, Enum):
    LOC: str = 'LOC'
    ORG: str = 'ORG'
    PER: str = 'PER'
