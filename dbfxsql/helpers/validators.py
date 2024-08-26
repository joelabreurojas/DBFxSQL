from collections.abc import Iterable

from pathlib import Path


def path_exists(sourcepath: str) -> None:
    return Path(sourcepath).exists()


def field_name_in(fields: Iterable[tuple], field_name: str) -> str:
    for field in fields:
        _field_name: str = field[0]

        if field_name.lower() == _field_name.lower():
            return _field_name


def values_are_different(rows: list[dict], row: dict) -> bool:
    """Checks if a list of rows are different from a given row."""

    for _row in rows:
        for key, value in row.items():
            if value != _row[key]:
                return True

    return False


def only_empty_records(rows: list) -> list:
    """Return an empty list if a list of rows only contains empty rows."""

    if not rows:
        return rows

    if [{""}] == [{row for row in rows.values()} for rows in rows]:
        return []

    return rows
