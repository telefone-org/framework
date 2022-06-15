import os
import sys
from typing import NoReturn

from watchfiles import awatch

from telefone.modules import logger


def restart() -> NoReturn:
    args = sys.argv.copy()
    args.insert(0, sys.executable)

    if sys.platform == "win32":
        args = [f'"{arg}"' for arg in args]

    os.chdir(os.getcwd())
    os.execv(sys.executable, args)


async def watch_to_reload(src_dir: str) -> None:
    """
    A coroutine that restarts the app when changes
    in source code are detected.
    :return:
    """
    async for _ in awatch(src_dir):
        logger.info("Changes were found. Restarting...")
        restart()
