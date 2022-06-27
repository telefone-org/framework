from typing import Dict, List, NamedTuple, Type, Union

from telefone_types.updates import BaseBotUpdate, BotUpdateType

from telefone.api.abc import ABCAPI
from telefone.framework.dispatch.dispenser.abc import ABCStateDispenser
from telefone.framework.dispatch.handler.abc import ABCHandler
from telefone.framework.dispatch.view.abc import ABCView
from telefone.modules import logger


class HandlerBasement(NamedTuple):
    dataclass: Union[dict, Type["BaseBotUpdate"]]
    handler: "ABCHandler"


class RawUpdateView(ABCView):
    handlers: Dict[BotUpdateType, List["HandlerBasement"]]

    def __init__(self) -> None:
        self.handlers = {}
        self.middlewares = []

    def get_handler_basements(self, update: dict) -> List["HandlerBasement"]:
        return self.handlers[BotUpdateType(self.get_update_type(update))]

    def get_update_model(
        self, handler_basement: "HandlerBasement", update: dict, ctx_api: "ABCAPI"
    ) -> Union[dict, "BaseBotUpdate"]:
        return handler_basement.dataclass(
            **update.get(self.get_update_type(update).value), unprepared_ctx_api=ctx_api
        )

    async def process_update(self, update: dict) -> bool:
        return self.get_update_type(update) in self.handlers

    async def handle_update(
        self,
        update: dict,
        ctx_api: "ABCAPI",
        state_dispenser: "ABCStateDispenser",
    ) -> None:
        logger.debug("Handling update with raw update view")

        context_variables: dict = {}
        handle_responses = []
        handlers = []

        mw_instances = await self.pre_middleware(update, context_variables)
        if mw_instances is None:
            logger.info("Pre middleware returned error; stopped handling")
            return

        for handler_basement in self.get_handler_basements(update):
            update_model = self.get_update_model(handler_basement, update, ctx_api)
            update_model.state_peer = await state_dispenser.cast(
                update_model.get_state_key()
            )

            result = await handler_basement.handler.filter(update_model)
            logger.debug("Handler {} returned {}", handler_basement.handler, result)

            if result is False:
                continue

            elif isinstance(result, dict):
                context_variables.update(result)

            handler_response = await handler_basement.handler.handle(
                update_model, **context_variables
            )
            handle_responses.append(handler_response)
            handlers.append(handler_basement.handler)

            if handler_basement.handler.blocking:
                break

        await self.post_middleware(mw_instances, handle_responses, handlers)
