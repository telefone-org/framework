import os
import sys
from typing import NoReturn

from telefone.modules import logger

STARTUP_DIR: str = os.getcwd()


def restart() -> NoReturn:
    args = sys.argv.copy()
    args.insert(0, sys.executable)

    if sys.platform == "win32":
        args = [f'"{arg}"' for arg in args]

    os.chdir(STARTUP_DIR)
    os.execv(sys.executable, args)


async def watch_to_reload(src_dir: str) -> None:
    """
    A coroutine that restarts the app when changes
    in source code are detected.
    :return:
    """
    try:
        from watchfiles import awatch
    except ImportError as e:
        raise SystemExit(
            "You need to install `watchfiles` package "
            "to be able to use auto_reload."
        ) from e

    async for _ in awatch(src_dir):
        logger.info("Changes were found. Restarting...")
        restart()
