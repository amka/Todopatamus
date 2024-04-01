from gi.repository import GObject
from gi.repository import Gom
from loguru import logger


class DbService(GObject.GObject):
    __gtype_name_ = 'DbService'

    path: str = GObject.Property(type=str)
    adapter: Gom.Adapter = None
    repository: Gom.Repository = None

    def __init__(self, path: str):
        self.adapter = Gom.Adapter()
        self.adapter.open_sync(path)
        self.repository = Gom.Repository(adapter=self.adapter)
        logger.debug("DbService initialized at {}", path)
