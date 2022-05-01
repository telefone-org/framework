from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Dict, Generic, List, TypeVar

if TYPE_CHECKING:
    from telefone.api.abc import ABCAPI
    from telefone.framework.dispatch.dispenser import ABCStateDispenser

from telefone.framework.dispatch.view.abc.view import ABCView
from telefone.modules import logger

T_contra = TypeVar("T_contra", list, dict, contravariant=True)


class ABCRawUpdateView(ABCView[T_contra], Generic[T_contra]):
    handlers: Dict[Any, List]

    @abstractmethod
    def get_handler_basements(self, update: T_contra) -> List:
        pass

    @abstractmethod
    def get_update_model(self, handler_basement, update: T_contra):
        pass

    @staticmethod
    @abstractmethod
    def get_update_type(update: T_contra):
        pass

    async def handle_update(
        self, update: T_contra, ctx_api: "ABCAPI", state_dispenser: "ABCStateDispenser"
    ) -> Any:
        logger.debug(
            "Handling update ({}) with message view".format(
                self.get_update_type(update)
            )
        )

        context_variables: dict = {}
        handle_responses = []
        handlers = []

        mw_instances = await self.pre_middleware(update, context_variables)
        if mw_instances is None:
            logger.info("Handling stopped, pre_middleware returned error")
            return

        for handler_basement in self.get_handler_basements(update):
            update_model = self.get_update_model(handler_basement, update)

            if isinstance(update_model, dict):
                update_model["ctx_api"] = ctx_api
            else:
                setattr(update_model, "unprepared_ctx_api", ctx_api)

            result = await handler_basement.handler.filter(update_model)
            logger.debug(
                "Handler {} returned {}".format(handler_basement.handler, result)
            )

            if result is False:
                continue

            elif isinstance(result, dict):
                context_variables.update(result)

            handler_response = await handler_basement.handler.handle(
                update_model, **context_variables
            )
            handle_responses.append(handler_response)
            handlers.append(handler_basement.handler)

            return_handler = self.handler_return_manager.get_handler(handler_response)
            if return_handler is not None:
                await return_handler(
                    self.handler_return_manager,
                    handler_response,
                    update_model,
                    context_variables,
                )

            if handler_basement.handler.blocking:
                break

        await self.post_middleware(mw_instances, handle_responses, handlers)
