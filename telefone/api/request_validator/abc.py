from abc import ABC, abstractmethod
from typing import NoReturn, Union


class ABCRequestValidator(ABC):
    @abstractmethod
    async def validate(self, request: dict) -> Union[dict, NoReturn]:
        pass
