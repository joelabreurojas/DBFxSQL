from dataclasses import dataclass, field
from watchfiles import Change, DefaultFilter


@dataclass
class WatchModified(DefaultFilter):
    allowed_extensions: tuple[str] = None
    _ignore_dirs: list = field(default_factory=list)
    _ignore_entity_regexes: list = field(default_factory=list)
    _ignore_paths: list = field(default_factory=list)

    def __call__(self, change: Change, path: str) -> bool:
        return (
            super().__call__(change, path)
            and change == Change.modified
            and path.endswith(self.allowed_extensions)
        )
