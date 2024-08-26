from ..models.error_template import ErrorTemplate


class SourceAlreadyExists(ErrorTemplate):
    def __init__(self, source: str):
        super().__init__(f"Source '{source}' already exists.")


class SourceNotFound(ErrorTemplate):
    def __init__(self, sourcepath: str):
        super().__init__(f"Source '{sourcepath}' not found.")
