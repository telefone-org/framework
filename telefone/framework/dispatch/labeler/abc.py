from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Union

from telefone_types.updates.types import BotUpdateType

from telefone.framework.dispatch.rule import ABCRule
from telefone.framework.dispatch.view import ABCView
from telefone.tools.mini_types import MessageMin

LabeledMessageHandler = Callable[..., Callable[[MessageMin], Any]]
LabeledHandler = Callable[..., Callable[[Any], Any]]


class ABCLabeler(ABC):
    @abstractmethod
    def message(self, *rules: "ABCRule", **custom_rules) -> LabeledMessageHandler:
        pass

    @abstractmethod
    def chat_message(self, *rules: "ABCRule", **custom_rules) -> LabeledMessageHandler:
        pass

    @abstractmethod
    def private_message(
        self, *rules: "ABCRule", **custom_rules
    ) -> LabeledMessageHandler:
        pass

    @abstractmethod
    def raw_update(
        self,
        update: Union[BotUpdateType, List[BotUpdateType]],
        dataclass: Callable = dict,
        *rules: "ABCRule",
        **custom_rules,
    ) -> LabeledHandler:
        pass

    @abstractmethod
    def views(self) -> Dict[str, "ABCView"]:
        pass

    @abstractmethod
    def load(self, labeler: Any):
        pass
