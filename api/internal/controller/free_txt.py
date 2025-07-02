from datetime import datetime, timedelta
from fastapi import Request
from loguru import logger
from core.settings import settings
from internal.common.schemas.free_txt import SummarizationRequest, SummarizationResponse


class FreeTxtController:
    async def summarization(
        self, sum_request: SummarizationRequest
    ) -> SummarizationResponse:
        text = "abceasoi"
        return SummarizationResponse(summarize_text=text)
