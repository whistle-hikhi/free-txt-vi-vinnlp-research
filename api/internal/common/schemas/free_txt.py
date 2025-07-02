from typing import Optional, List

from pydantic import BaseModel, Field

from internal.common.enums.free_txt import EnumSentimentLabel


class Entry(BaseModel):
    review: str = Field(description="Sentence")
    sentiment_label: EnumSentimentLabel = Field(description="Sentiment Label")


class MeaningAnalysisResponse(BaseModel):
    catergorise: int = Field(description="Sentiment Categorize")
    entries: List[Entry] = Field(description="Sentiment Info")


class SentimentChartWord(BaseModel):
    word: str = Field(description="Word to search")
    positive_frequency: int = Field(description="Positive Frequency")
    negative_neutral_frequency: int = Field(
        description="Negative and Neutral Frequency"
    )
    score: int = Field(description="Score sentiment")


class SentimentChartResponse(BaseModel):
    words: List[SentimentChartWord] = Field(description="List word to represent")


class SummarizationRequest(BaseModel):
    text: str = Field(description="Input text")


class SummarizationResponse(BaseModel):
    summarize_text: str = Field(description="Summarized Text")


class WordCloudWord(BaseModel):
    word: str = Field(description="Word")
    score: int = Field(description="Score to view")


class WordCloudResponse(BaseModel):
    words: List[WordCloudWord] = Field(description="Many words and their score")


class WordTreeWord(BaseModel):
    keyword: str = Field(description="Keyword in word tree")
    prefix: dict = Field(description="Prefix")
    suffix: dict = Field(description="Suffix")


class WordTreeResponse(BaseModel):
    keywords: List[WordTreeWord] = Field(description="List of words")


class SentenceEntry(BaseModel):
    left_context: str = Field(description="Left Context")
    keyword: str = Field(description="Keyword")
    right_context: str = Field(description="Right Context")


class WordEntry(BaseModel):
    word: str = Field(description="Word")
    frequency: int = Field(description="Frequency")
    mutual_information: float = Field(description="Mutual Information")
    log_likelihood: float = Field(description="Log Likelihood")


class WordUseRelationshipsResponse(BaseModel):
    sentences: List[SentenceEntry] = Field(description="Sentences")
    words: List[WordEntry] = Field(description="Words")
