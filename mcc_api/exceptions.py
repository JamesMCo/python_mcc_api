import typing as t


class MCCAPIError(BaseException):
    """The base exception from which all other mcc_api exceptions inherit."""

    code: int
    """Response code of the request from the API."""
    reason: t.Optional[str]
    """Reason for the response code, if applicable."""

    def __init__(self: t.Self, code: int, reason: t.Optional[str]) -> None:
        self.code = code
        self.reason = reason

        super().__init__(f"MCC API returned code {self.code}" + f": \"{self.reason}\"" if self.reason else "")


class InvalidEventError(MCCAPIError):
    """Exception raised when the requested event does not exist."""
    pass


class InvalidGameError(MCCAPIError):
    """Exception raised when the requested game does not exist."""
    pass


class InvalidTeamError(MCCAPIError):
    """Exception raised when the requested team does not exist."""
    pass


class RateLimitError(MCCAPIError):
    """Exception raised when the MCC API returns a rate limit error."""
    pass
