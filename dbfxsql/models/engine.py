from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Engine:
    folderpaths: list[str]
    extensions: list[str]
    db_server: str | None = None
    db_user: str | None = None
    db_password: str | None = None
    convert_to_extension: list = field(default_factory=list)
