from db.models.base import Base
from db.models.models import *  # noqa: F403
from db.session import engine


def init_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)
