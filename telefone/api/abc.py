from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Optional

from telefone.http.abc import ABCHTTPClient

if TYPE_CHECKING:
    from telefone.http import ABCHTTPClient

    from .request_rescheduler import ABCRequestRescheduler
    from .request_validator import ABCRequestValidator
    from .response_validator import ABCResponseValidator


class ABCAPI(ABC):
    ignore_errors: bool
    http_client: "ABCHTTPClient"
    request_rescheduler: "ABCRequestRescheduler"
    response_validators: List["ABCResponseValidator"]
    request_validators: List["ABCRequestValidator"]

    @abstractmethod
    async def request(
        self,
        method: str,
        data: Optional[dict] = None,
    ) -> dict:
        pass
