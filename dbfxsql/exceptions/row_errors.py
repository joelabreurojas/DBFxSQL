from ..models.error_template import ErrorTemplate


class RowNotFound(ErrorTemplate):
    def __init__(self, condition: tuple):
        super().__init__(f"Row not found with: {''.join(condition)}")


class RowAlreadyExists(ErrorTemplate):
    def __init__(self, row_id: int):
        super().__init__(f"Row already exists with id: {row_id}")
