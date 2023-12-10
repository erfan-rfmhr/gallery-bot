from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base

_engine = create_engine('sqlite:///gallery.sqlite3')


def get_engine():
    return _engine


def create_db():
    Base.metadata.create_all(_engine)


def get_session():
    session = sessionmaker(bind=_engine)
    return session()
