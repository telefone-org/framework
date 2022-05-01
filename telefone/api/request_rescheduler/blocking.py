import typing
from time import sleep as blocking_sleep

from telefone.api.request_rescheduler.abc import ABCRequestRescheduler
from telefone.modules import logger

if typing.TYPE_CHECKING:
    from telefone.api import ABCAPI, API


DEFAULT_DELAY = 5


class BlockingRequestRescheduler(ABCRequestRescheduler):
    def __init__(self, delay: int = DEFAULT_DELAY):
        self.delay = delay

    async def reschedule(
        self,
        ctx_api: typing.Union["ABCAPI", "API"],
        method: str,
        data: dict,
        recent_response: typing.Any,
    ) -> dict:
        logger.debug(
            "Telefone uses a request rescheduler when Telegram "
            "doesn't respond properly for an amount of time. Starting..."
        )

        attempt_number = 1
        while not isinstance(recent_response, dict):
            logger.info(f"Attempt {attempt_number}. Making request...")
            blocking_sleep(self.delay * attempt_number)
            recent_response = await ctx_api.request(method, data)
            attempt_number += 1
            logger.debug(f"Attempt succeed? - {isinstance(recent_response, dict)}")

        logger.info(f"Finally succeed after {self.delay ** attempt_number} seconds!")
        return recent_response
