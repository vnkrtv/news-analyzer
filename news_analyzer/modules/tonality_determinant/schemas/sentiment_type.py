from enum import Enum


class SentimentType(str, Enum):
    NEUTRAL: str = 'neutral'
    NEGATIVE: str = 'negative'
    POSITIVE: str = 'positive'
    SKIP: str = 'skip'
    SPEECH: str = 'speech'
