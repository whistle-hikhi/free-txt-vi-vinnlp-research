from internal.common.exceptions.common import XBaseException


class ExceptionNoReferenceTextWordCloud(XBaseException):
    def __init__(self):
        super().__init__(
            status_code=400,
            message=f"reference_text is required for log-likelihood/keyness",
        )
