from typing import TYPE_CHECKING, Dict, List, NamedTuple, Type, Union

from telefone_types.updates import BotUpdateType

from telefone.framework.dispatch.return_manager.base import BotMessageReturnManager
from telefone.framework.dispatch.view.abc.raw import ABCRawUpdateView

if TYPE_CHECKING:
    from telefone_types.updates.base import BaseBotUpdate

    from telefone.framework.dispatch.handler import ABCHandler


class BotHandlerBasement(NamedTuple):
    dataclass: Union[Type[dict], Type["BaseBotUpdate"]]
    handler: "ABCHandler"


class BotRawUpdateView(ABCRawUpdateView[dict]):
    handlers: Dict[BotUpdateType, List["BotHandlerBasement"]]

    def __init__(self):
        super().__init__()
        self.handlers = {}
        self.handler_return_manager = BotMessageReturnManager()

    def get_handler_basements(self, update: dict) -> List["BotHandlerBasement"]:
        return self.handlers[BotUpdateType(self.get_update_type(update))]

    def get_update_model(
        self, handler_basement: "BotHandlerBasement", update: dict
    ) -> Union[dict, "BaseBotUpdate"]:
        return handler_basement.dataclass(**update.get(self.get_update_type(update)))

    @staticmethod
    def get_update_type(update: dict) -> str:
        update_copy = update.copy()
        update_copy.pop("update_id")
        return list(update_copy)[0]

    async def process_update(self, update: dict) -> bool:
        return BotUpdateType(self.get_update_type(update)) in self.handlers
