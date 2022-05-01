import typing
from abc import ABC, abstractmethod

from telefone.api.abc import ABCAPI
from telefone.exception_factory import ABCErrorHandler
from telefone.framework.dispatch.dispenser.abc import ABCStateDispenser
from telefone.framework.dispatch.view.abc import ABCView


class ABCRouter(ABC):
    views: typing.Dict[str, "ABCView"]
    state_dispenser: ABCStateDispenser
    error_handler: ABCErrorHandler

    @abstractmethod
    async def route(self, update: dict, api: "ABCAPI") -> typing.Any:
        pass

    @abstractmethod
    def construct(
        self,
        views: typing.Dict[str, "ABCView"],
        state_dispenser: ABCStateDispenser,
        error_handler: ABCErrorHandler,
    ) -> "ABCRouter":
        pass

    def add_view(self, name: str, view: "ABCView") -> typing.NoReturn:
        self.views[name] = view

    def view(self, name: str) -> typing.Callable[..., typing.Type["ABCView"]]:
        def decorator(view: typing.Type["ABCView"]):
            self.add_view(name, view())
            return view

        return decorator
