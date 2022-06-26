from abc import ABC, abstractmethod
from typing import Any, Callable, Coroutine, Dict, List, Optional, Type, Union

from telefone_types.updates import BaseBotUpdate

from telefone.api import ABCAPI, API
from telefone.framework.dispatch.dispenser.abc import ABCStateDispenser
from telefone.framework.dispatch.handler.abc import ABCHandler
from telefone.framework.dispatch.handler.func import FromFuncHandler
from telefone.framework.dispatch.middleware.base import BaseMiddleware
from telefone.framework.dispatch.return_manager.abc import ABCReturnManager
from telefone.framework.dispatch.rule.abc import ABCRule
from telefone.modules import logger


class ABCView(ABC):
    handler_return_manager: Optional["ABCReturnManager"]
    handlers: Union[List["ABCHandler"], Dict[Any, List[Any]]]
    middlewares: List[Type["BaseMiddleware"]]

    @abstractmethod
    async def process_update(self, update: dict) -> bool:
        pass

    @abstractmethod
    async def handle_update(
        self,
        update: dict,
        ctx_api: "ABCAPI",
        state_dispenser: "ABCStateDispenser",
    ) -> None:
        pass

    @staticmethod
    @abstractmethod
    def get_update_model(
        update: dict, ctx_api: Union["ABCAPI", "API"]
    ) -> "BaseBotUpdate":
        pass

    async def pre_middleware(
        self,
        update: dict,
        context_variables: Optional[dict] = None,
    ) -> Optional[List[BaseMiddleware]]:
        """
        Run all of the pre middleware methods
        and return an exception if any error occurs
        """
        mw_instances = []

        for middleware in self.middlewares:
            mw_instance = middleware(update, view=self)
            await mw_instance.pre()
            if not mw_instance.can_forward:
                logger.debug(f"Pre middleware {mw_instance} returned error {mw_instance.error}")
                return None

            mw_instances.append(mw_instance)

            if context_variables is not None:
                context_variables.update(mw_instance.context_update)

        return mw_instances

    async def post_middleware(
        self,
        mw_instances: List[BaseMiddleware],
        handle_responses: Optional[List] = None,
        handlers: Optional[List["ABCHandler"]] = None,
    ):
        for middleware in mw_instances:
            middleware.handle_responses = (
                handle_responses or middleware.handle_responses
            )
            middleware.handlers = handlers or middleware.handlers

            await middleware.post()
            if not middleware.can_forward:
                logger.debug(
                    f"Post middleware {middleware} returned error {middleware.error!r}"
                )
                return middleware.error

    def register_middleware(self, middleware: Type[BaseMiddleware]):
        try:
            if not issubclass(middleware, BaseMiddleware):
                raise ValueError("Argument is not a subclass of BaseMiddleware")
        except TypeError:
            raise ValueError("Argument is not a class")
        self.middlewares.append(middleware)

    @staticmethod
    def get_update_type(update: dict) -> str:
        update_copy = update.copy()
        update_copy.pop("update_id")
        return list(update_copy)[0]

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            f"handlers={self.handlers} "
            f"middlewares={self.middlewares} "
            f"handler_return_manager={self.handler_return_manager}"
        )
