from dataclasses import dataclass
from typing import Any, Self

from ..exceptions import FieldNotFound, ValueNotValid


@dataclass(slots=True)
class Condition:
    _field: str
    _operator: str
    _value: Any

    def __post_init__(self: Self) -> None:
        self.field = self._field
        self.operator = self._operator
        self.value = self._value

    def __str__(self: Self) -> str:
        self.operator: str = self._operator

        return f"{self._field}{self._operator}{self._value}"

    @property
    def field(self: Self) -> str:
        return self._field

    @field.setter
    def field(self, field: str) -> None:
        self._field = field.lower()

    @property
    def operator(self) -> str:
        return self._operator

    @operator.setter
    def operator(self, operator: str) -> None:
        self._operator = "=" if operator == "==" else operator

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        try:
            self._value = int(self._value) if "row_number" == self._field else value
        except ValueError:
            raise ValueNotValid(self._value, self._field, "int")

    def apply_filter(self: Self, row_: dict, index: int | None = None) -> str:
        row: dict = row_.copy()  # shallow copy to avoid side effects

        if isinstance(index, int):
            row["row_number"] = index + 1

        if not row.get(self._field):
            raise FieldNotFound(self._field)

        operator: str = "==" if self._operator == "=" else self._operator

        if operator not in ["==", "!=", ">", ">=", "<", "<="]:
            return False

        if isinstance(row[self._field], str):
            return f"'{row[self._field]}'{operator}'{self._value}'"

        return f"{row[self._field]}{operator}{self._value}"
