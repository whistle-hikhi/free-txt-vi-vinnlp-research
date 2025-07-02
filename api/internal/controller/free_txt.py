from datetime import datetime, timedelta
from fastapi import Request
from loguru import logger
from core.settings import settings
from internal.common.schemas.free_txt import SummarizationRequest, SummarizationResponse
from internal.services.summarisation import summa_summarizer


class FreeTxtController:
    async def summarization(
        self, sum_request: SummarizationRequest
    ) -> SummarizationResponse:
        text = await summa_summarizer(sum_request.text, sum_request.ratio)
        return SummarizationResponse(summarize_text=text)
