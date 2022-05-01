from abc import ABC, abstractmethod
from typing import Any, AsyncIterator, Optional

from telefone.api.abc import ABCAPI
from telefone.exception_factory import ABCErrorHandler


class ABCPolling(ABC):
    @abstractmethod
    async def get_updates(self) -> Any:
        pass

    @abstractmethod
    async def listen(self) -> AsyncIterator[dict]:
        pass

    @property
    @abstractmethod
    def api(self) -> "ABCAPI":
        pass

    @api.setter
    def api(self, new_api: "ABCAPI"):
        pass

    @abstractmethod
    def construct(
        self, api: "ABCAPI", error_handler: Optional["ABCErrorHandler"] = None
    ) -> "ABCPolling":
        pass
