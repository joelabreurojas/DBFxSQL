from ..models.error_template import ErrorTemplate


class ValueNotValid(ErrorTemplate):
    """Error raised when a value is not valid for a given field and type."""

    def __init__(self, value: int | str, field: str, type_: str):
        super().__init__(
            f"Value '{value}' not valid for field '{field}' with type '{type_}'"
        )
