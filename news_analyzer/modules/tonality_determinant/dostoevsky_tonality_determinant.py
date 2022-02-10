from typing import Dict

from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

from .base_tonality_determanant import BaseTonalityDeterminant
from .schemas.sentiment_type import SentimentType


class DostoevskyTonalityDeterminant(BaseTonalityDeterminant):
    tokenizer: RegexTokenizer = RegexTokenizer()
    model: FastTextSocialNetworkModel = FastTextSocialNetworkModel(tokenizer=tokenizer)

    def get_tonality(self, text: str) -> Dict[SentimentType, float]:
        return self.model.predict([text])[0]
