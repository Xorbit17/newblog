from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from sqlalchemy.ext.declarative import declarative_base


class Database(object):
    """Singleton object"""

    def __init__(self, database_connection_string, create_schema=True):
        self.engine = create_engine(database_connection_string, echo=True)
        self.engine.connect()

        self._Session = sessionmaker()
        self._Session.configure(bind=self.engine)

    def create_schema(self, base):
        base.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        return self._Session()

    def dispose(self):
        self.engine.dispose()
