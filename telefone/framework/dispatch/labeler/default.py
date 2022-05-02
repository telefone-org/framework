import re
from typing import Any, Dict, List, Type, Union

from vbml import Patcher

from telefone.framework.dispatch.handler.func import FromFuncHandler
from telefone.framework.dispatch.labeler.abc import (
    ABCLabeler,
    LabeledHandler,
    LabeledMessageHandler,
    UpdateName,
)
from telefone.framework.dispatch.rule.abc import ABCRule
from telefone.framework.dispatch.rule.bot import (
    CommandRule,
    CoroutineRule,
    FuncRule,
    LevensteinRule,
    MatchRule,
    MessageLengthRule,
    PeerRule,
    RegexRule,
    StateGroupRule,
    StateRule,
)
from telefone.framework.dispatch.view.abc import ABCView
from telefone.framework.dispatch.view.default.message import BotMessageView
from telefone.framework.dispatch.view.default.raw import (
    BotHandlerBasement,
    BotRawUpdateView,
)
from telefone_types.updates import BaseBotUpdate, BotUpdateType


DEFAULT_CUSTOM_RULES: Dict[str, Type[ABCRule]] = {
    "text": MatchRule,
    "command": CommandRule,
    "regex": RegexRule,
    "regexp": RegexRule,
    "state": StateRule,
    "state_group": StateGroupRule,
    "func": FuncRule,
    "function": FuncRule,
    "coro": CoroutineRule,
    "coroutine": CoroutineRule,
    "levenstein": LevensteinRule,
    "lev": LevensteinRule,
    "from_chat": PeerRule,
    "length": MessageLengthRule,
}


class Labeler(ABCLabeler):
    def __init__(self, **kwargs):
        self.message_view = BotMessageView()
        self.raw_update_view = BotRawUpdateView()

        self.custom_rules = kwargs.get("custom_rules") or DEFAULT_CUSTOM_RULES
        self.auto_rules: List["ABCRule"] = []

        self.rule_config: Dict[str, Any] = {
            "vbml_flags": re.MULTILINE,  # Flags for VBMLRule
            "vbml_patcher": Patcher(),  # Patcher for VBMLRule
        }

    @property
    def vbml_ignore_case(self) -> bool:
        """Gets ignore case flag from rule config flags"""
        return re.IGNORECASE in self.rule_config["flags"]

    @vbml_ignore_case.setter
    def vbml_ignore_case(self, ignore_case: bool):
        """Adds ignore case flag to rule config flags or removes it"""
        if not ignore_case:
            self.rule_config["vbml_flags"] ^= re.IGNORECASE
        else:
            self.rule_config["vbml_flags"] |= re.IGNORECASE

    @property
    def vbml_patcher(self) -> Patcher:
        return self.rule_config["vbml_patcher"]

    @vbml_patcher.setter
    def vbml_patcher(self, patcher: Patcher):
        self.rule_config["vbml_patcher"] = patcher

    @property
    def vbml_flags(self) -> re.RegexFlag:
        return self.rule_config["vbml_flags"]

    @vbml_flags.setter
    def vbml_flags(self, flags: re.RegexFlag):
        self.rule_config["vbml_flags"] = flags

    def message(
        self, *rules: "ABCRule", blocking: bool = True, **custom_rules
    ) -> "LabeledMessageHandler":
        assert all(
            isinstance(rule, ABCRule) for rule in rules
        ), "All rules must be subclasses of ABCRule or rule shortcuts"

        def decorator(func):
            self.message_view.handlers.append(
                FromFuncHandler(
                    func,
                    *rules,
                    *self.auto_rules,
                    *self.get_custom_rules(custom_rules),
                    blocking=blocking,
                )
            )
            return func

        return decorator

    def chat_message(
        self, *rules: "ABCRule", blocking: bool = True, **custom_rules
    ) -> "LabeledMessageHandler":
        assert all(
            isinstance(rule, ABCRule) for rule in rules
        ), "All rules must be subclasses of ABCRule or rule shortcuts"

        def decorator(func):
            self.message_view.handlers.append(
                FromFuncHandler(
                    func,
                    PeerRule(True),
                    *rules,
                    *self.auto_rules,
                    *self.get_custom_rules(custom_rules),
                    blocking=blocking,
                )
            )
            return func

        return decorator

    def private_message(
        self,
        *rules: "ABCRule",
        blocking: bool = True,
        **custom_rules,
    ) -> "LabeledMessageHandler":
        assert all(
            isinstance(rule, ABCRule) for rule in rules
        ), "All rules must be subclasses of ABCRule or rule shortcuts"

        def decorator(func):
            self.message_view.handlers.append(
                FromFuncHandler(
                    func,
                    PeerRule(False),
                    *rules,
                    *self.auto_rules,
                    *self.get_custom_rules(custom_rules),
                    blocking=blocking,
                )
            )
            return func

        return decorator

    def raw_update(
        self,
        update: Union[UpdateName, List[UpdateName]],
        dataclass: Union[Type[dict], Type["BaseBotUpdate"]] = dict,
        *rules: "ABCRule",
        blocking: bool = True,
        **custom_rules,
    ) -> "LabeledHandler":
        assert all(
            isinstance(rule, ABCRule) for rule in rules
        ), "All rules must be subclasses of ABCRule or rule shortcuts"

        if not isinstance(update, list):
            update = [update]

        def decorator(func):
            for u in update:
                if isinstance(u, str):
                    u = BotUpdateType(u)
                handler_basement = BotHandlerBasement(
                    dataclass,
                    FromFuncHandler(
                        func,
                        *rules,
                        *self.auto_rules,
                        *self.get_custom_rules(custom_rules),
                        blocking=blocking,
                    ),
                )
                update_handlers = self.raw_update_view.handlers.setdefault(u, [])
                update_handlers.append(handler_basement)
            return func

        return decorator

    def load(self, labeler: "Labeler"):
        self.message_view.handlers.extend(labeler.message_view.handlers)
        self.message_view.middlewares.extend(labeler.message_view.middlewares)
        self.raw_update_view.middlewares.extend(labeler.raw_update_view.middlewares)

        for event, handler_basements in labeler.raw_update_view.handlers.items():
            event_handlers = self.raw_update_view.handlers.setdefault(event, [])
            event_handlers.extend(handler_basements)

    def get_custom_rules(self, custom_rules: Dict[str, Any]) -> List["ABCRule"]:
        return [self.custom_rules[k].with_config(self.rule_config)(v) for k, v in custom_rules.items()]  # type: ignore

    def views(self) -> Dict[str, "ABCView"]:
        return {"message": self.message_view, "raw": self.raw_update_view}
