from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Config:
    engines: dict[str, dict]
    relations: list[dict]
