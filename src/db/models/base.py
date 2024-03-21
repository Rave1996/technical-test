import uuid

from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase

from core.utils.datetime import LocalTime


class Base(DeclarativeBase):
    pass


class UUIDMixin:
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)  # noqa: A003


class TimeStampedMixin:
    created = Column(DateTime(timezone=True), default=LocalTime.now)
    modified = Column(DateTime(timezone=True), default=LocalTime.now, onupdate=func.now())


class BaseModel(Base, UUIDMixin, TimeStampedMixin):
    __abstract__ = True

    def dict(self):  # noqa: A003
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        return self.__str__()
