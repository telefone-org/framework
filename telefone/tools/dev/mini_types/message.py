import typing

from telefone_types import Message, StatePeer

from telefone.api import ABCAPI, API


class MessageMin(Message):
    unprepared_ctx_api: typing.Optional[typing.Any] = None
    state_peer: typing.Optional[StatePeer] = None

    @property
    def ctx_api(self) -> typing.Union["ABCAPI", "API"]:
        return getattr(self, "unprepared_ctx_api")

    async def answer(
        self,
        text: str,
        chat_id: typing.Optional[int] = None,
        disable_web_page_preview: typing.Optional[bool] = None,
        disable_notification: typing.Optional[bool] = None,
        reply_markup: typing.Optional[dict] = None,
        parse_mode: typing.Optional[str] = None,
    ) -> Message:
        params = {k: v for k, v in locals().items() if k != "self" and v is not None}
        params["chat_id"] = chat_id or self.chat.id

        return await self.ctx_api.send_message(**params)

    async def reply(
        self,
        text: str,
        disable_web_page_preview: typing.Optional[bool] = None,
        disable_notification: typing.Optional[bool] = None,
        reply_markup: typing.Optional[dict] = None,
        parse_mode: typing.Optional[str] = "MarkdownV2",
    ) -> Message:
        params = {k: v for k, v in locals().items() if k != "self" and v is not None}
        params["chat_id"] = self.chat.id
        params["reply_to_message_id"] = self.message_id

        return await self.ctx_api.send_message(**params)

    async def forward(
        self,
        chat_id: typing.Union[int, str],
        disable_notification: typing.Optional[bool] = None,
    ) -> Message:
        params = {k: v for k, v in locals().items() if k != "self" and v is not None}
        params["from_chat_id"] = self.chat.id
        params["message_id"] = self.message_id

        return await self.ctx_api.forward_message(**params)


MessageMin.update_forward_refs()


def message_min(update: dict, ctx_api: "ABCAPI") -> "MessageMin":
    message = MessageMin(**update["message"])
    setattr(message, "unprepared_ctx_api", ctx_api)
    return message
