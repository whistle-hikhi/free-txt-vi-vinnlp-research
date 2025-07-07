from datetime import datetime, timedelta
from fastapi import Request
from loguru import logger
from core.settings import settings
from internal.common.schemas.free_txt import (
    SummarizationRequest,
    SummarizationResponse,
    WordTreeRequest,
    WordTreeResponse,
    WordCloudRequest,
    WordCloudResponse,
)
from internal.services.summarisation import Summarizer
from internal.services.word_tree import WordTree
from internal.services.word_cloud import WordCloud


class FreeTxtController:
    summarizer: Summarizer
    wordtree: WordTree

    def __init__(self):
        self.summarizer = Summarizer()
        self.wordtree = WordTree()
        self.wordcloud = WordCloud()

    async def summarization(
        self, sum_request: SummarizationRequest
    ) -> SummarizationResponse:
        text = await self.summarizer.sum_qwen(sum_request.text, sum_request.ratio)
        return SummarizationResponse(summarize_text=text)

    async def gen_wordtree(self, wordtree_request: WordTreeRequest) -> WordTreeResponse:
        tree = await self.wordtree.build_word_tree(
            wordtree_request.text, wordtree_request.keyword
        )
        return WordTreeResponse(
            word=tree["word"], left=tree["left"], right=tree["right"]
        )

    async def gen_wordcloud(
        self, wordcloud_request: WordCloudRequest
    ) -> WordCloudResponse:
        word_stats = await self.wordcloud.gen_wordcloud(wordcloud_request)

        return WordCloudResponse(words=word_stats)
