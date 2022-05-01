from typing import (
    Any,
    AsyncIterator,
    Iterable,
    List,
    NamedTuple,
    NoReturn,
    Optional,
    Union,
)

from telefone_types.methods import APIMethods

from telefone.api.abc import ABCAPI
from telefone.api.request_rescheduler import (
    ABCRequestRescheduler,
    BlockingRequestRescheduler,
)
from telefone.api.request_validator import (
    DEFAULT_REQUEST_VALIDATORS,
    ABCRequestValidator,
)
from telefone.api.response_validator import (
    DEFAULT_RESPONSE_VALIDATORS,
    ABCResponseValidator,
)
from telefone.http.abc import ABCHTTPClient
from telefone.http.default import SingleAioHTTPClient
from telefone.modules import logger

APIRequest = NamedTuple("APIRequest", [("method", str), ("data", dict)])


class API(ABCAPI, APIMethods):
    API_URL = "https://api.telegram.org/"
    APIRequest = APIRequest

    def __init__(
        self,
        token: str,
        ignore_errors: bool = False,
        http_client: Optional["ABCHTTPClient"] = None,
        request_rescheduler: Optional[ABCRequestRescheduler] = None,
    ):
        super().__init__(self)

        self.token = token
        self.ignore_errors = ignore_errors
        self.request_url = self.API_URL + f"bot{self.token}/"
        self.http_client = http_client or SingleAioHTTPClient()
        self.request_rescheduler = request_rescheduler or BlockingRequestRescheduler()
        self.request_validators: List[ABCRequestValidator] = DEFAULT_REQUEST_VALIDATORS
        self.response_validators: List[
            ABCResponseValidator
        ] = DEFAULT_RESPONSE_VALIDATORS

    async def request(self, method: str, data: Optional[dict] = None) -> dict:
        """Makes a single request opening a session"""
        data = await self.validate_request(data)
        response = await self.http_client.request_text(
            url=self.request_url + method,
            method="POST",
            data=data,
        )

        logger.debug(
            "Request {} with {} data returned {}".format(method, data, response)
        )
        return await self.validate_response(method, data, response)

    async def request_many(
        self, requests: Iterable[APIRequest]  # type: ignore
    ) -> AsyncIterator[dict]:
        for request in requests:
            method, data = request.method, await self.validate_request(request.data)  # type: ignore
            response = await self.http_client.request_text(
                url=self.request_url + method,
                method="POST",
                data=data,
            )
            logger.debug(
                "Request {} with {} data returned {}".format(method, data, response)
            )
            yield await self.validate_response(method, data, response)

    async def validate_response(
        self, method: str, data: dict, response: Union[dict, str]
    ) -> Union[Any, NoReturn]:
        """Validates response from Telegram,
        to change validations change API.response_validators (list of ResponseValidator's)"""
        for validator in self.response_validators:
            response = await validator.validate(method, data, response, self)  # type: ignore
        logger.debug("API response was validated")
        return response  # type: ignore

    async def validate_request(self, request: dict) -> dict:
        """Validates requests from Telegram,
        to change validations change API.request_validators (list of RequestValidator's)"""
        for validator in self.request_validators:
            request = await validator.validate(request)  # type: ignore
        logger.debug("API request was validated")
        return request  # type: ignore
