"""
All known exceptions of Samenloop package
"""


class SamenLopenError(Exception):
    pass


class HTTPError(SamenLopenError):
    pass


class ConfigurationError(SamenLopenError):
    pass


class UnknownValue(SamenLopenError):
    pass


class UnknownResource(SamenLopenError):
    pass


class EnvVars(SamenLopenError):
    pass


class TooLongTMR(SamenLopenError):
    pass


class APIRateLimitReached(SamenLopenError):
    pass

class TimeOut(SamenLopenError):
    pass
