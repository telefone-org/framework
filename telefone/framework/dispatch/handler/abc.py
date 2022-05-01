from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from telefone_types.objects import Update


class ABCHandler(ABC):
    blocking: bool

    @abstractmethod
    async def filter(self, update: "Update") -> Union[dict, bool]:
        pass

    @abstractmethod
    async def handle(self, update: "Update", **context) -> Any:
        pass
