from .error_template import ErrorTemplate


class DBFConnectionFailed(ErrorTemplate):
    """Error raised when a dBase database connection fails."""

    def __init__(self, source: str, error: Exception):
        super().__init__(f"dBase connection with `{source}` failed.\n{error}")


class SQLConnectionFailed(ErrorTemplate):
    """Error raised when a SQL database connection fails."""

    def __init__(self, engine: str, source: str, error: Exception):
        super().__init__(f"{engine} connection with `{source}` failed.\n{error}")
