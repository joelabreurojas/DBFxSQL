from .error_template import ErrorTemplate


class FolderPathNotProvided(ErrorTemplate):
    def __init__(self, engine: str):
        super().__init__(f"Folderpath not provided for engine '{engine}' in config.")
