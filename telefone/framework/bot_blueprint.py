from typing import Optional

from telefone.api import ABCAPI
from telefone.framework.abc_blueprint import ABCBlueprint
from telefone.framework.bot import Bot
from telefone.framework.dispatch.labeler import Labeler
from telefone.framework.dispatch.router.base import Router
from telefone.framework.polling import ABCPolling
from telefone.modules import logger


class Blueprint(ABCBlueprint):
    def __init__(
        self,
        name: Optional[str] = None,
        labeler: Optional[Labeler] = None,
        router: Optional[Router] = None,
    ):
        if name is not None:
            self.name = name

        self.labeler = labeler or Labeler()
        self.router: Router = router or Router()
        self.constructed = False

    def construct(self, api: ABCAPI, polling: ABCPolling) -> "Blueprint":
        self.api = api
        self.polling = polling
        self.constructed = True
        return self

    def load(self, framework: "Bot") -> "Blueprint":
        framework.labeler.load(self.labeler)  # type: ignore
        logger.debug(f"Blueprint {self.name!r} loaded")
        return self.construct(framework.api, framework.polling)

    @property
    def on(self) -> Labeler:
        return self.labeler
