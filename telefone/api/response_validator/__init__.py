from .abc import ABCResponseValidator
from .json_validator import JSONResponseValidator
from .telegram_api_error_validator import TelegramAPIErrorResponseValidator

DEFAULT_RESPONSE_VALIDATORS = [
    JSONResponseValidator(),
    TelegramAPIErrorResponseValidator(),
]
