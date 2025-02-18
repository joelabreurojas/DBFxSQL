from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Engine:
    folderpaths: list[str]
    extensions: list[str]
    db_server: str | None
    db_user: str | None
    db_password: str | None
