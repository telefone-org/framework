from io import BytesIO
from pathlib import Path
from typing import Optional, Union

from aiofiles import open


class File:
    def __init__(
        self, name: Optional[str] = None, file_source: Optional[bytes] = None
    ) -> None:
        self.name, self.file_source = name, file_source

    @classmethod
    def from_bytes(cls, file_source: bytes, name: str) -> "File":
        return cls(name=name, file_source=file_source)

    @classmethod
    async def from_path(
        cls, file_source: Union[str, Path], name: Optional[str] = None
    ) -> "File":
        path = Path(file_source) if isinstance(file_source, str) else path

        async with open(path, "rb") as f:
            return cls(name=name or path.name, file_source=await f.read())

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r}>"
