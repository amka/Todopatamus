from gi.repository import Gom
from gi.repository import GObject


class DbService(GObject.GObject):
    __gtype_name_ = 'DbService'

    path: str = GObject.Property(type=str)
    adapter: Gom.Adapter = None

    def __init__(self, path: str):
        self.adapter = Gom.Adapter()
        self.adapter.open_sync(path)
