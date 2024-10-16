import sys


class ErrorTemplate(Exception):
    """Base class for custom error messages."""

    def __init__(self, message: str):
        self.message = message
        sys.exit(self)

    def __str__(self) -> str:
        return f"Error: {self.message}"
