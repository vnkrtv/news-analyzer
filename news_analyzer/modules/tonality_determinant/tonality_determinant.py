from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

from .base_tonality_determanant import BaseTonalityDeterminant
from .schemas.text_tonality import TextTonality


class TonalityDeterminant(BaseTonalityDeterminant):
    tokenizer: RegexTokenizer = RegexTokenizer()
    model: FastTextSocialNetworkModel = FastTextSocialNetworkModel(tokenizer=tokenizer)

    def get_tonality(self, text: str) -> TextTonality:
        tonality = self.model.predict([text])
        return TextTonality(
            text=text,
            tonality=tonality
        )
