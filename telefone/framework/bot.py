from asyncio import AbstractEventLoop, get_event_loop
from typing import NoReturn, Optional, Union

from telefone.api import ABCAPI, API
from telefone.exception_factory import ABCErrorHandler, ErrorHandler
from telefone.framework.abc import ABCFramework
from telefone.framework.dispatch import (
    ABCLabeler,
    ABCRouter,
    BuiltinStateDispenser,
    Labeler,
    Router,
)
from telefone.framework.polling import ABCPolling, Polling
from telefone.modules import logger
from telefone.tools.dev.loop_wrapper import LoopWrapper


class Bot(ABCFramework):
    def __init__(
        self,
        token: Optional[str] = None,
        api: Optional[ABCAPI] = None,
        polling: Optional[ABCPolling] = None,
        router: Optional["ABCRouter"] = None,
        labeler: Optional["ABCLabeler"] = None,
        loop: Optional[AbstractEventLoop] = None,
        loop_wrapper: Optional[LoopWrapper] = None,
        error_handler: Optional["ABCErrorHandler"] = None,
        task_each_update: bool = True,
    ):
        self.api: Union[ABCAPI, API] = API(token) if token is not None else api  # type: ignore
        self.error_handler = error_handler or ErrorHandler()
        self.loop_wrapper = loop_wrapper or LoopWrapper()
        self.labeler = labeler or Labeler()
        self.state_dispenser = BuiltinStateDispenser()
        self._polling: "ABCPolling" = polling or Polling(self.api)
        self._router: "ABCRouter" = router or Router()
        self._loop = loop
        self.task_each_update = task_each_update

    async def run_polling(
        self, offset: int = 0, allowed_updates: list[str] = []
    ) -> NoReturn:
        self.polling.offset, self.polling.allowed_updates = offset, allowed_updates
        logger.info("Polling will be started")

        async for update in self.polling.listen():  # type: ignore
            logger.debug("Received update: {}", update)
            self.loop.create_task(self.router.route(update, self.api))

    def run_forever(self):
        logger.info("Loop will be ran until stopped")
        self.loop_wrapper.add_task(self.run_polling())
        self.loop_wrapper.run_forever(self.loop)  # type: ignore

    @property
    def on(self) -> "ABCLabeler":
        return self.labeler

    @property
    def polling(self) -> "ABCPolling":
        return self._polling.construct(self.api)

    @property
    def router(self) -> "ABCRouter":
        return self._router.construct(
            views=self.labeler.views(),
            state_dispenser=self.state_dispenser,
            error_handler=self.error_handler,
        )

    @property
    def loop(self) -> AbstractEventLoop:
        if self._loop is None:
            self._loop = get_event_loop()
        return self._loop

    @loop.setter
    def loop(self, new_loop: AbstractEventLoop):
        self._loop = new_loop

    @router.setter
    def router(self, new_router: "ABCRouter"):
        self._router = new_router

    @polling.setter
    def polling(self, value):
        self._polling = value
