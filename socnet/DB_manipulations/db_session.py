from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from socnet.DB_manipulations.db import Base


def get_engine(user, passwd, db):
    """
    Connects to database
    """
    url = f'postgresql://{user}:{passwd}@db/{db}'
    pass
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url, pool_size=50, echo=False)
    return engine


def get_session(engine):
    """
    Makes session
    """
    session = sessionmaker(bind=engine)()
    return session


def session_init():
    engine = get_engine('postgres',
                        'postgres',
                        'postgres',)

    Base.metadata.create_all(engine)
    session = get_session(engine)
    return session
