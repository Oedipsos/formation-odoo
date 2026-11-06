import contextlib
import functools

import psycopg2
from psycopg2.extensions import connection as Connection
from psycopg2.extras import RealDictCursor

from refuge.config import db_settings


class DatabaseConnection:
    def __init__(self, settings: dict[str, str] | None = None):
        self.settings = settings or db_settings()
        self.dbname = self.settings["dbname"]
        self.open = False

    def __enter__(self) -> DatabaseConnection:
        self._conn = psycopg2.connect(**self.settings)
        self.open = True

        print(f"Connected to database {self.dbname!r}")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.rollback()
            print(f"Connection to {self.dbname!r} closed after error: {exc_value}")
        else:
            print(f"Connection to {self.dbname!r} closed.")

        self.close()
        self.open = False

    @staticmethod
    def _if_open(method):
        """Use this method to decorate functions that must be
        called only if the database connection is open
        """

        @functools.wraps(method)
        def wrap(self, *args, **kwargs):
            if not self.open:
                raise RuntimeError(f"Connection to {self.dbname!r} is not open.")
            return method(self, *args, **kwargs)

        return wrap

    def close(self):
        return self._conn.close()

    @_if_open
    def rollback(self):
        return self._conn.rollback()

    @_if_open
    def commit(self):
        return self._conn.commit()

    @_if_open
    def cursor(self) -> RealDictCursor:
        return self._conn.cursor(cursor_factory=RealDictCursor)

    @contextlib.contextmanager
    @_if_open
    def transaction(self):
        try:
            yield
            self.commit()
        except RuntimeError:
            self.rollback()
            raise
