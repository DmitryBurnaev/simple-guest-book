import argparse
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


if os.environ.get('TEST_ENV'):
    PATH_TO_DATABASE = os.environ.get('PATH_TEST_DATABASE', '/tmp/test.db')
    if os.path.exists(PATH_TO_DATABASE):
        os.remove(PATH_TO_DATABASE)
else:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PATH_TO_DATABASE = os.path.join(base_dir, 'data.db')


engine = create_engine('sqlite:///{}'.format(PATH_TO_DATABASE),
                       convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def create_db():
    from src import models
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--createdb', action='store_true', default=False)
    args = parser.parse_args()
    if args.createdb:
        create_db()
