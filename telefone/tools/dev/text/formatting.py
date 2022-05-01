from typing import Optional


class Text:
    def __init__(self, text: Optional[str] = None) -> None:
        self.text = text or str()

    def regular(self, text: str) -> "Text":
        self.text += text
        return self

    def bold(self, text: str) -> "Text":
        self.text += f"<b>{text}</b>"
        return self

    def italic(self, text: str) -> "Text":
        self.text += f"<i>{text}</i>"
        return self

    def code(self, text: str) -> "Text":
        self.text += f"<code>{text}</code>"
        return self

    def line_break(self, n: int) -> "Text":
        self.text += "\n" * n
        return self

    def space(self, n: int) -> "Text":
        self.text += " " * n
        return self

    def to_string(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return self.text
