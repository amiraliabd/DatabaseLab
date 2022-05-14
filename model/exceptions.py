class DBException(Exception):
    pass


class NotFound(DBException):
    pass


class IntegrityError(DBException):
    pass
