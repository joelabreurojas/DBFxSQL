from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Relation:
    sources: list[str]
    tables: list[str]
    fields: list[list[str]]
    priority: str | None
