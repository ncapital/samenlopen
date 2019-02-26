"""
All known exceptions of Samenloop package
"""


class SamenLoopError(Exception):
    pass


class HTTPError(SamenLoopError):
    pass


class ConfigurationError(SamenLoopError):
    pass


class UnknownValue(SamenLoopError):
    pass


class EnvVars(SamenLoopError):
    pass


class TooLongTMR(SamenLoopError):
    pass


class APIRateLimitReached(SamenLoopError):
    pass
