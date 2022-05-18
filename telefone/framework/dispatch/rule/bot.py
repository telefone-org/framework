import inspect
import re
from abc import abstractmethod
from typing import Awaitable, Callable, Coroutine, List, Optional, Tuple, Type, Union

from vbml import Patcher, Pattern

from telefone.framework.dispatch.rule.abc import ABCRule
from telefone.tools.dev.mini_types.message import MessageMin

from telefone_types.states import BaseStateGroup, get_state_repr


DEFAULT_PREFIXES = ["!", "/"]
Message = MessageMin


class ABCMessageRule(ABCRule):
    @abstractmethod
    async def check(self, message: Message) -> bool:
        pass


class CommandRule(ABCMessageRule):
    def __init__(
        self,
        command_text: Union[str, Tuple[str, int]],
        prefixes: Optional[List[str]] = None,
        args_count: int = 0,
        sep: str = " ",
    ):
        self.prefixes = prefixes or DEFAULT_PREFIXES
        self.command_text = (
            command_text if isinstance(command_text, str) else command_text[0]
        )
        self.args_count = (
            args_count if isinstance(command_text, str) else command_text[1]
        )
        self.sep = sep

    async def check(self, message: Message) -> Union[dict, bool]:
        for prefix in self.prefixes:
            if self.args_count == 0 and message.text == prefix + self.command_text:
                return True
            if self.args_count > 0 and message.text.startswith(
                prefix + self.command_text + " "
            ):
                args = message.text[len(prefix + self.command_text) + 1 :].split(
                    self.sep
                )
                if len(args) != self.args_count:
                    return False
                elif any(len(arg) == 0 for arg in args):
                    return False
                return {"args": tuple(args)}
        return False


class CoroutineRule(ABCMessageRule):
    def __init__(self, coroutine: Coroutine):
        self.coro = coroutine

    async def check(self, message: Message) -> Union[dict, bool]:
        return await self.coro


class FuncRule(ABCMessageRule):
    def __init__(self, func: Callable[[Message], Union[bool, Awaitable]]):
        self.func = func

    async def check(self, message: Message) -> Union[dict, bool]:
        if inspect.iscoroutinefunction(self.func):
            return await self.func(update)  # type: ignore
        return self.func(update)  # type: ignore


class LevensteinRule(ABCMessageRule):
    def __init__(
        self,
        levenstein_texts: Union[List[str], str],
        max_distance: int = 1,
    ):
        if isinstance(levenstein_texts, str):
            levenstein_texts = [levenstein_texts]
        self.levenstein_texts = levenstein_texts
        self.max_distance = max_distance

    @staticmethod
    def distance(a: str, b: str) -> int:
        n, m = len(a), len(b)
        if n > m:
            a, b = b, a
            n, m = m, n

        current_row = range(n + 1)
        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n  # type: ignore
            for j in range(1, n + 1):
                add, delete, change = (
                    previous_row[j] + 1,
                    current_row[j - 1] + 1,
                    previous_row[j - 1],
                )
                if a[j - 1] != b[i - 1]:
                    change += 1
                current_row[j] = min(add, delete, change)  # type: ignore

        return current_row[n]

    async def check(self, message: Message) -> bool:
        for levenstein_text in self.levenstein_texts:
            if self.distance(message.text, levenstein_text) <= self.max_distance:
                return True
        return False


class MatchRule(ABCMessageRule):
    def __init__(
        self,
        pattern: Union[str, "Pattern", List[Union[str, "Pattern"]]],
        patcher: Optional["Patcher"] = None,
        flags: Optional[re.RegexFlag] = None,
    ):
        flags = flags or self.config.get("vbml_flags")

        if isinstance(pattern, str):
            pattern = [Pattern(pattern, flags=flags or self.config.get("vbml_flags"))]
        elif isinstance(pattern, Pattern):
            pattern = [pattern]
        elif isinstance(pattern, list):
            pattern = [
                p
                if isinstance(p, Pattern)
                else Pattern(p, flags=flags or self.config.get("vbml_flags"))
                for p in pattern
            ]

        self.patterns = pattern
        self.patcher = patcher or self.config["vbml_patcher"]

    async def check(self, message: Message) -> Union[dict, bool]:
        for pattern in self.patterns:
            result = self.patcher.check(pattern, message.text)
            if result not in (None, False):
                return result
        return False


class MessageLengthRule(ABCMessageRule):
    def __init__(self, min_length: int):
        self.min_length = min_length

    async def check(self, message: Message) -> bool:
        return len(message.text) >= self.min_length


class PeerRule(ABCMessageRule):
    def __init__(self, from_chat: bool = True):
        self.from_chat = from_chat

    async def check(self, message: Message) -> bool:
        if message.chat.id != message.from_.id:
            return self.from_chat
        return not self.from_chat


class RegexRule(ABCMessageRule):
    def __init__(
        self,
        regexp: Union[str, List[str], Pattern, List[Pattern]],
    ):
        if isinstance(regexp, Pattern):
            regexp = [regexp]
        elif isinstance(regexp, str):
            regexp = [re.compile(regexp)]
        elif isinstance(regexp, list):
            regexp = [re.compile(exp) for exp in regexp]

        self.regexp = regexp

    async def check(self, message: Message) -> Union[dict, bool]:
        for regexp in self.regexp:
            match = re.match(regexp, message.text)
            if match:
                return {"match": match.groups()}
        return False


class ReplyMessageRule(ABCMessageRule):
    async def check(self, message: Message) -> bool:
        if not message.reply_to_message:
            return False
        return True


class StateRule(ABCMessageRule):
    def __init__(
        self,
        state: Optional[Union[List["BaseStateGroup"], "BaseStateGroup"]] = None,
    ):
        if not isinstance(state, list):
            state = [] if state is None else [state]
        self.state = [get_state_repr(s) for s in state]

    async def check(self, event: Message) -> bool:
        if event.state_peer is None:
            return not self.state
        return event.state_peer.state in self.state


class StateGroupRule(ABCMessageRule):
    def __init__(
        self,
        state_group: Union[List[Type[BaseStateGroup]], Type[BaseStateGroup]],
    ):
        if not isinstance(state_group, list):
            state_group = [] if state_group is None else [state_group]
        self.state_group = state_group

    async def check(self, message: Message) -> bool:
        if message.state_peer is None:
            return not self.state_group
        return type(message.state_peer.state) in self.state_group
