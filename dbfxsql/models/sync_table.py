from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SyncTable:
    engine: str
    source: str
    name: str
    fields: list[str]
    records: list[dict]
