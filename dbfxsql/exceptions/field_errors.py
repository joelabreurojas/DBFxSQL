from .error_template import ErrorTemplate


class FieldNotFound(ErrorTemplate):
    """Error raised when a field is not found in a table."""

    def __init__(self, field: str):
        super().__init__(f"Field '{field}' not found.")


class FieldReserved(ErrorTemplate):
    """Error raised when a field is reserved."""

    def __init__(self, field: str):
        super().__init__(f"Field '{field}' is reserved and cannot be assigned.")
