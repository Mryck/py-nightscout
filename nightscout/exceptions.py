"""Exceptions for NS."""


class NSError(Exception):
    """Generic NS exception."""

    pass


class NSConnectionError(NSError):
    """NS connection exception."""

    pass
