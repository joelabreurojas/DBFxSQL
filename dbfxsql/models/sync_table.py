from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class SyncTable:
    engine: str
    source: str
    name: str
    fields: list[str]
    rows: list | None = None
