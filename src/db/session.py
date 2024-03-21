from types import TracebackType

from loguru import logger
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from core.settings import settings

application_name = settings.PROJECT_NAME.replace(" ", "-").lower()
engine = create_engine(settings.POSTGRESQL_URL.unicode_string(), connect_args={"application_name": application_name})


class DatabaseSessionManager:
    def __init__(self, engine: Engine) -> None:
        self.SessionManager = scoped_session(sessionmaker(bind=engine, autocommit=False))

    def __enter__(self) -> Session:
        self.db = self.SessionManager()
        return self.db

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        try:
            if exc_type is not None:
                self.db.rollback()
        except Exception as error:
            logger.exception(error.__str__())
            self.db.rollback()
            raise error  # noqa: TRY201
        finally:
            self.db.close()
            self.SessionManager.remove()


def use_session() -> Session:
    try:
        return DatabaseSessionManager(engine)
    except Exception as exc:
        logger.exception(exc.__str__())


DBSession = sessionmaker(bind=engine, autocommit=False)


def get_session():
    db = DBSession()
    try:
        yield db
    except Exception as ex:
        db.rollback()
        logger.exception(ex.__str__())
