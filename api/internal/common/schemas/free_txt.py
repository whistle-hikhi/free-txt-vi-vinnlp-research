from typing import Optional, List

from pydantic import BaseModel, Field

from internal.common.enums.free_txt import EnumSentimentLabel, EnumWordCloudMeasure


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
    ratio: float = Field(description="Ratio of summary")


class SummarizationResponse(BaseModel):
    summarize_text: str = Field(description="Summarized Text")


class WordCloudRequest(BaseModel):
    text: str
    reference_text: str = None  # Needed for log-likelihood/keyness
    measurement_type: EnumWordCloudMeasure = Field("Measurement type")


class WordStat(BaseModel):
    word: str = Field(description="Word")
    weight: float = Field(description="Score to view")


class WordCloudResponse(BaseModel):
    words: List[WordStat] = Field(description="Many words and their score")


class WordTreeRequest(BaseModel):
    text: str = Field(description="Input text")
    keyword: str = Field(description="Keyword in word tree")


class WordTreeResponse(BaseModel):
    word: str = Field(description="Keyword")
    left: dict = Field(description="Left side")
    right: dict = Field(description="Right side")


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
