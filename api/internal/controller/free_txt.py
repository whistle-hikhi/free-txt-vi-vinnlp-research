from datetime import datetime, timedelta
from fastapi import Request
from loguru import logger
from core.settings import settings
from internal.common.schemas.free_txt import SummarizationRequest, SummarizationResponse
from internal.services.summarisation import Summarizer


class FreeTxtController:
    summarizer: Summarizer

    def __init__(self):
        self.summarizer = Summarizer()

    async def summarization(
        self, sum_request: SummarizationRequest
    ) -> SummarizationResponse:
        text = await self.summarizer.summarizer_summa(
            sum_request.text, sum_request.ratio
        )
        return SummarizationResponse(summarize_text=text)
