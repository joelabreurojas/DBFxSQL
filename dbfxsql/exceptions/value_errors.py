from ..models.error_template import ErrorTemplate


class ValueNotValid(ErrorTemplate):
    """Error raised when a value is not valid for a given field and type."""

    def __init__(self, value: str, field: str, _type: str):
        super().__init__(
            f"Value '{value}' not valid for field '{field}' with type '{_type}'"
        )
