import os

from gi.repository import GLib
from playhouse.sqlite_ext import SqliteExtDatabase


class DbService:
    _path: str = os.path.join(GLib.get_user_data_dir(), 'todos.db')
    db = SqliteExtDatabase(None)

    def initialize(self, path: str = None):
        if path and os.path.exists(path):
            self._path = path

        try:
            self.db.init(self._path, pragmas={'journal_mode': 'wal'})
            print(f"DbService loaded db at path: {self._path}")

        except Exception as e:
            print(f"Failed to initialize: {e}")
            self.db.close()


db_service = DbService()
