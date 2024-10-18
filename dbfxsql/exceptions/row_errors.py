from ..models.error_template import ErrorTemplate


class RowNotFound(ErrorTemplate):
    def __init__(self, condition: str):
        super().__init__(f"Row not found with: {condition}")


class RowAlreadyExists(ErrorTemplate):
    def __init__(self, row_id: int):
        super().__init__(f"Row already exists with id: {row_id}")
