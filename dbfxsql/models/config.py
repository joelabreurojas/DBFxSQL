from dataclasses import dataclass

from .engine import Engine
from .relation import Relation


@dataclass(frozen=True, slots=True)
class Config:
    engines: list[Engine]
    relations: list[Relation]
