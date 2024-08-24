"""Structures focused on the transmission of information throughout the application"""

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class User:
    """Class for keeping track of an existing user"""

    id: int | None = None
    name: str | None = None
    password: str | None = None
