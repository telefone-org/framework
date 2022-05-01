from abc import ABC
from typing import TYPE_CHECKING, Generic, Optional, TypeVar

from telefone_types.updates import BotUpdateType

from telefone.framework.dispatch.return_manager.base import BotMessageReturnManager
from telefone.framework.dispatch.view.abc import ABCMessageView
from telefone.tools.dev.mini_types.message import message_min

if TYPE_CHECKING:
    from telefone.tools.dev.mini_types.message import MessageMin


T_contra = TypeVar("T_contra", contravariant=True)


class ABCBotMessageView(ABCMessageView[dict, T_contra], ABC, Generic[T_contra]):
    def __init__(self):
        super().__init__()
        self.handler_return_manager = BotMessageReturnManager()

    @staticmethod
    def get_update_type(update: dict) -> str:
        update_copy = update.copy()
        update_copy.pop("update_id")
        return list(update_copy)[0]

    @staticmethod
    async def get_message(update, ctx_api) -> "MessageMin":
        return message_min(update, ctx_api)

    async def process_update(self, update: dict) -> bool:
        return BotUpdateType(self.get_update_type(update)) == BotUpdateType.MESSAGE


class BotMessageView(ABCBotMessageView["MessageMin"]):
    def get_state_key(self, message: "MessageMin") -> Optional[int]:
        return getattr(message, self.state_source_key, None)
