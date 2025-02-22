from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class SyncTable:
    engine: str
    source: str
    name: str
    fields: list
    rows: list = field(default_factory=list)
