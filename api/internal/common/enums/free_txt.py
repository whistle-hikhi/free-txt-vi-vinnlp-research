from enum import Enum


class EnumSentimentLabel(str, Enum):
    POSITIVE = "POSITIVE"
    NEUTRAL = "NEUTRAL"
    NEGATIVE = "NEGATIVE"
    VERY_POSITIVE = "VERY_POSTIVE"
    VERY_NEGATIVE = "VERY_NEGATIVE"
