from typing import AsyncIterator, List, Optional

from telefone.api import ABCAPI
from telefone.exception_factory import ABCErrorHandler, ErrorHandler, TelegramAPIError
from telefone.framework.polling.abc import ABCPolling
from telefone.modules import logger


class Polling(ABCPolling):
    def __init__(
        self,
        api: Optional[ABCAPI] = None,
        error_handler: Optional[ABCErrorHandler] = None,
        offset: Optional[int] = None,
        allowed_updates: Optional[List[str]] = None,
    ):
        self._api = api
        self._error_handler = error_handler or ErrorHandler()
        self._stop = False

        self.offset, self.allowed_updates = offset, allowed_updates

    async def get_updates(self) -> Optional[List[dict]]:
        raw_updates = []

        # try:
        raw_updates = await self.api.request(
            "getUpdates",
            {"offset": self.offset, "allowed_updates": self.allowed_updates},
        )
        # except TelegramAPIError[401, 404] as e:
        #     logger.critical(e)
        #     self.stop()

        return raw_updates

    async def listen(self) -> AsyncIterator[dict]:
        self._stop = False

        while not self._stop:
            try:
                updates = await self.get_updates()
                for update in updates:
                    self.offset = update["update_id"] + 1
                    yield update
            except BaseException as e:
                await self._error_handler.handle(e)

    def stop(self) -> None:
        self._stop = True

    def construct(
        self, api: "ABCAPI", error_handler: Optional["ABCErrorHandler"] = None
    ) -> "Polling":
        self._api = api
        if error_handler is not None:
            self._error_handler = error_handler
        return self

    @property
    def api(self) -> "ABCAPI":
        if self._api is None:
            self.stop()
            raise NotImplementedError(
                "You must construct polling with API "
                "before try to access api property of Polling"
            )
        return self._api

    @api.setter
    def api(self, new_api: "ABCAPI"):
        self._api = new_api
