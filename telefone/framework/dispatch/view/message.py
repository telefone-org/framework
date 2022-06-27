from typing import Union

from telefone_types.updates import BotUpdateType, MessageUpdate

from telefone.api import ABCAPI, API
from telefone.framework.dispatch.dispenser.abc import ABCStateDispenser
from telefone.framework.dispatch.return_manager.message import MessageReturnManager
from telefone.framework.dispatch.view.abc import ABCView
from telefone.modules import logger


class MessageView(ABCView):
    def __init__(self) -> None:
        self.handlers = []
        self.middlewares = []
        self.default_text_approximators = []
        self.handler_return_manager = MessageReturnManager()

    @staticmethod
    def get_update_model(update: dict, ctx_api: Union["ABCAPI", "API"]) -> "MessageUpdate":
        return MessageUpdate(**update["message"], unprepared_ctx_api=ctx_api)

    async def process_update(self, update: dict) -> bool:
        return self.get_update_type(update) == BotUpdateType.MESSAGE

    async def handle_update(
        self, update: dict, ctx_api: "ABCAPI", state_dispenser: "ABCStateDispenser"
    ) -> None:
        logger.debug("Handling update with message view")

        message = self.get_update_model(update, ctx_api)
        message.state_peer = await state_dispenser.cast(message.get_state_key())

        context_variables = {}
        mw_instances = await self.pre_middleware(message, context_variables)

        if mw_instances is None:
            logger.info("Stopping handling because pre middleware returned error")
            return

        handlers = []
        handle_responses = []

        for handler in self.handlers:
            response = await handler.filter(message)
            logger.debug("Handler {} returned {}", handler, response)

            if response is False:
                continue

            elif isinstance(response, dict):
                context_variables.update(response)

            handler_response = await handler.handle(message, **context_variables)
            handle_responses.append(handler_response)
            handlers.append(handler)

            return_handler = self.handler_return_manager.get_handler(handler_response)
            if return_handler is not None:
                await return_handler(
                    self.handler_return_manager,
                    handler_response,
                    message,
                    context_variables,
                )

            if handler.blocking:
                break

        await self.post_middleware(mw_instances, handle_responses, handlers)
