from typing import TYPE_CHECKING, Union

from telefone.framework.dispatch.return_manager import ABCReturnManager

if TYPE_CHECKING:
    from telefone.tools.mini_types.message import MessageMin


class BotMessageReturnManager(ABCReturnManager):
    @ABCReturnManager.instance_of(str)
    async def str_handler(self, value: str, message: "MessageMin", _: dict):
        await message.answer(value)

    @ABCReturnManager.instance_of((tuple, list))
    async def iter_handler(
        self, value: Union[tuple, list], message: "MessageMin", _: dict
    ):
        [await message.answer(str(e)) for e in value]

    @ABCReturnManager.instance_of(dict)
    async def dict_handler(self, value: dict, message: "MessageMin", _: dict):
        await message.answer(**value)
