from sqlalchemy.exc import NoResultFound


class ObjectNotFound(NoResultFound):
    def __init__(self, message, data=None):
        super().__init__(message)
        self.data = data or {}


class ObjectAlreadyExistsError(Exception):
    def __init__(self, message, data=None):  # noqa: ARG002
        super().__init__(message)
