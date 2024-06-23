class InvalidToken(Exception):
    """Raise when the given API token is invalid"""


class Unsupported(Exception):
    """Raise when the given engine is not supported"""


class ConnectionFailed(Exception):
    """Raise when unable to connect to engine"""
