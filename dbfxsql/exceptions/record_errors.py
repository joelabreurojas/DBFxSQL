from ..models.error_template import ErrorTemplate


class RecordNotFound(ErrorTemplate):
    def __init__(self, condition: str):
        super().__init__(f"Record not found with: {condition}")


class RecordAlreadyExists(ErrorTemplate):
    def __init__(self, record_id: int):
        super().__init__(f"Record already exists with id: {record_id}")
