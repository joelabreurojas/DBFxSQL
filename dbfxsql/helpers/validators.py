from collections.abc import Iterable

from dbfxsql.helpers import formatters, file_manager

from pathlib import Path
from watchfiles import Change


def path_exists(filepath: str) -> None:
    filepath = Path(filepath)

    return filepath.exists()


def field_name_in(fields: Iterable[tuple], field_name_: str) -> str:
    for field in fields:
        field_name: str = field[0]

        if field_name_.lower() == field_name.lower():
            return field_name


def only_empty_records(rows: list) -> list:
    """Return an empty list if a list of rows only contains empty rows."""

    if not rows:
        return rows

    if [{""}] == [{row for row in rows.values()} for rows in rows]:
        return []

    return rows


def same_rows(origin_row: dict, destiny_row: dict, fields: tuple) -> bool:
    for origin_field, destiny_field in zip(*fields):
        if origin_row[origin_field] != destiny_row[destiny_field]:
            return False

    return True


def only_modified(change: Change, path: str) -> bool:
    return change == Change.modified


def values_are_different(rows: list[dict], row_: dict) -> bool:
    """Checks if a list of rows are different from a given row."""

    for row in rows:
        for key, value in row_.items():
            if value != row[key]:
                return True

    return False


def valid_filepath(filepath_: str, engines: dict) -> bool:
    filepath = Path(filepath_)

    extension: str = filepath.suffix
    folderpath: str = str(filepath.resolve().parent)

    for engine in engines.values():
        folderpaths: list = [str(Path(f).resolve()) for f in engine["folderpaths"]]

        if extension in engine["extensions"]:
            if folderpath in folderpaths:
                return True

    return False


def check_engine(filename: str) -> str | None:
    extension: str = formatters.decompose_file(filename)[1]
    engines: dict = file_manager.load_config()["engines"]

    for engine_name, engine_config in engines.items():
        if extension in engine_config["extensions"]:
            return engine_name
