from requests.auth import AuthBase
from requests import PreparedRequest
import typing as t


class APIKey(AuthBase):
    key: str

    def __init__(self: "APIKey", key: str) -> None:
        self.key = key

    def __eq__(self: "APIKey", other: t.Any) -> bool:
        if isinstance(other, str):
            return str(self) == other
        elif isinstance(other, APIKey):
            return self.key == other.key
        else:
            return False

    def __ne__(self: "APIKey", other: t.Any) -> bool:
        return not self == other

    def __call__(self: "APIKey", r: PreparedRequest) -> PreparedRequest:
        r.headers["X-API-Key"] = str(self)
        return r

    def __str__(self: "APIKey") -> str:
        return self.key
