import typing

from telefone.api.response_validator.abc import ABCResponseValidator
from telefone.exception_factory import TelegramAPIError

if typing.TYPE_CHECKING:
    from telefone.api import ABCAPI, API


class TelegramAPIErrorResponseValidator(ABCResponseValidator):
    async def validate(
        self,
        _,
        data: dict,
        response: typing.Any,
        ctx_api: typing.Union["ABCAPI", "API"],
    ) -> typing.Union[typing.Any, typing.NoReturn]:
        if response.get("ok"):
            return response.get("result")

        code, msg = response.get("error_code"), response.get("description")

        if ctx_api.ignore_errors:
            return None

        raise TelegramAPIError[code](msg, data)
