import os

from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DSN = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'data.db'))
DSN = os.environ.get('FLASK_DB_PATH') or DSN

engine = create_engine(DSN, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    try:
        from src import models
    except InvalidRequestError:
        pass
    Base.metadata.create_all(bind=engine)


