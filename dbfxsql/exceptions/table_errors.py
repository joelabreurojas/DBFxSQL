from .error_template import ErrorTemplate


class TableAlreadyExists(ErrorTemplate):
    def __init__(self, table_name: str):
        super().__init__(f"Table '{table_name}' already exists.")


class TableNotFound(ErrorTemplate):
    def __init__(self, table_name: str):
        super().__init__(f"Table '{table_name}' not found.")
