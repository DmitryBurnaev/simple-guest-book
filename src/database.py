import argparse
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_DSN = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'data.db'))
engine = create_engine(DB_DSN, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    print(DB_DSN)
    from src import models
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--createdb', action='store_true', default=False)
    args = parser.parse_args()
    if args.createdb:
        init_db()
